from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services import chamado_service
from app.repositories import responsavel_repo
from app.models.domain import Prioridade, Status

bp = Blueprint('chamado', __name__)

@bp.route('/')
def dashboard():
    filtro_status = request.args.get('status')
    filtro_prioridade = request.args.get('prioridade')
    
    if filtro_status == 'TODOS': filtro_status = None
    if filtro_prioridade == 'TODOS': filtro_prioridade = None

    chamados = chamado_service.listar_chamados(status=filtro_status, prioridade=filtro_prioridade)
    responsaveis = {r.id: r.nome for r in responsavel_repo.listar_todos()}
    
    return render_template(
        'dashboard.html', 
        chamados=chamados, 
        responsaveis=responsaveis,
        filtro_status=filtro_status,
        filtro_prioridade=filtro_prioridade,
        Prioridade=Prioridade,
        Status=Status
    )

@bp.route('/chamados/novo', methods=['GET'])
def novo_chamado():
    responsaveis = responsavel_repo.listar_todos()
    return render_template('chamado_form.html', responsaveis=responsaveis, Prioridade=Prioridade)

@bp.route('/chamados', methods=['POST'])
def criar_chamado():
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    prioridade_str = request.form.get('prioridade')
    atribuicao_auto = request.form.get('atribuicao_automatica') == 'on'
    responsavel_id = request.form.get('responsavel_id')
    
    if not titulo or not descricao or not prioridade_str:
        flash("Todos os campos obrigatórios devem ser preenchidos.", "error")
        return redirect(url_for('chamado.novo_chamado'))
        
    try:
        prioridade = Prioridade(prioridade_str)
        dados = chamado_service.ChamadoCreateDTO(
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            atribuicao_automatica=atribuicao_auto,
            responsavel_id=int(responsavel_id) if responsavel_id and not atribuicao_auto else None
        )
        chamado_service.criar_chamado(dados)
        flash("Chamado criado com sucesso!", "success")
        return redirect(url_for('chamado.dashboard'))
    except Exception as e:
        flash(f"Erro ao criar chamado: {str(e)}", "error")
        return redirect(url_for('chamado.novo_chamado'))

@bp.route('/chamados/<int:id>', methods=['GET'])
def visualizar_chamado(id):
    try:
        chamado = chamado_service.obter_chamado(id)
        responsavel = responsavel_repo.obter_por_id(chamado.responsavel_id)
        return render_template('chamado_view.html', chamado=chamado, responsavel=responsavel, Status=Status)
    except ValueError:
        flash("Chamado não encontrado.", "error")
        return redirect(url_for('chamado.dashboard'))

@bp.route('/chamados/<int:id>/editar', methods=['GET'])
def editar_chamado(id):
    try:
        chamado = chamado_service.obter_chamado(id)
        return render_template('chamado_form.html', chamado=chamado, Prioridade=Prioridade, Status=Status)
    except ValueError:
        flash("Chamado não encontrado.", "error")
        return redirect(url_for('chamado.dashboard'))

@bp.route('/chamados/<int:id>/editar', methods=['POST'])
def atualizar_chamado(id):
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    prioridade_str = request.form.get('prioridade')
    status_str = request.form.get('status')
    
    try:
        dados = chamado_service.ChamadoUpdateDTO(
            chamado_id=id,
            prioridade=Prioridade(prioridade_str),
            status=Status(status_str),
            titulo=titulo,
            descricao=descricao
        )
        chamado_service.atualizar_chamado(dados)
        flash("Chamado atualizado com sucesso!", "success")
        return redirect(url_for('chamado.visualizar_chamado', id=id))
    except Exception as e:
        flash(f"Erro ao atualizar chamado: {str(e)}", "error")
        return redirect(url_for('chamado.editar_chamado', id=id))