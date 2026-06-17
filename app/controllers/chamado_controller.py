from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services import chamado_service
from app.repositories import responsavel_repo
from app.models.domain import Prioridade, Status
from app.forms import ChamadoCreateForm, ChamadoUpdateForm
import math

bp = Blueprint('chamado', __name__)

ITEMS_PER_PAGE = 10

@bp.route('/')
def dashboard():
    page = request.args.get('page', 1, type=int)
    filtro_status = request.args.get('status')
    filtro_prioridade = request.args.get('prioridade')
    
    if filtro_status == 'TODOS': filtro_status = None
    if filtro_prioridade == 'TODOS': filtro_prioridade = None

    chamados, total_items = chamado_service.listar_chamados_paginado(
        page=page,
        per_page=ITEMS_PER_PAGE,
        status=filtro_status, 
        prioridade=filtro_prioridade
    )
    
    responsaveis = {r.id: r.nome for r in responsavel_repo.listar_todos()}
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    return render_template(
        'dashboard.html', 
        chamados=chamados, 
        responsaveis=responsaveis,
        page=page,
        total_pages=total_pages,
        filtro_status=filtro_status,
        filtro_prioridade=filtro_prioridade,
        Prioridade=Prioridade,
        Status=Status
    )


@bp.route('/chamados/novo', methods=['GET', 'POST'])
def novo_chamado():
    form = ChamadoCreateForm()
    # Popula dinamicamente as escolhas do responsável
    form.responsavel_id.choices = [(r.id, r.nome) for r in responsavel_repo.listar_todos()]

    if form.validate_on_submit():
        try:
            dados = chamado_service.ChamadoCreateDTO(
                titulo=form.titulo.data,
                descricao=form.descricao.data,
                prioridade=Prioridade(form.prioridade.data),
                atribuicao_automatica=form.atribuicao_automatica.data,
                responsavel_id=form.responsavel_id.data if not form.atribuicao_automatica.data else None
            )
            chamado_service.criar_chamado(dados)
            flash("Chamado criado com sucesso!", "success")
            return redirect(url_for('chamado.dashboard'))
        except Exception as e:
            flash(f"Erro ao criar chamado: {str(e)}", "error")
    
    return render_template('chamado_form.html', form=form, title="Novo Chamado")


@bp.route('/chamados/<int:id>', methods=['GET'])
def visualizar_chamado(id):
    try:
        chamado = chamado_service.obter_chamado(id)
        responsavel = responsavel_repo.obter_por_id(chamado.responsavel_id)
        return render_template('chamado_view.html', chamado=chamado, responsavel=responsavel, Status=Status)
    except ValueError:
        flash("Chamado não encontrado.", "error")
        return redirect(url_for('chamado.dashboard'))

@bp.route('/chamados/<int:id>/editar', methods=['GET', 'POST'])
def editar_chamado(id):
    try:
        chamado = chamado_service.obter_chamado(id)
    except ValueError:
        flash("Chamado não encontrado.", "error")
        return redirect(url_for('chamado.dashboard'))

    form = ChamadoUpdateForm(obj=chamado)

    if form.validate_on_submit():
        try:
            dados = chamado_service.ChamadoUpdateDTO(
                chamado_id=id,
                titulo=form.titulo.data,
                descricao=form.descricao.data,
                prioridade=Prioridade(form.prioridade.data),
                status=Status(form.status.data)
            )
            chamado_service.atualizar_chamado(dados)
            flash("Chamado atualizado com sucesso!", "success")
            return redirect(url_for('chamado.visualizar_chamado', id=id))
        except Exception as e:
            flash(f"Erro ao atualizar chamado: {str(e)}", "error")
            
    # Na requisição GET, preenche o formulário com os dados do banco.
    elif request.method == 'GET':
        form.titulo.data = chamado.titulo
        form.descricao.data = chamado.descricao
        form.prioridade.data = chamado.prioridade.value
        form.status.data = chamado.status.value

    return render_template('chamado_form.html', form=form, title=f"Editar Chamado #{id}", chamado=chamado)