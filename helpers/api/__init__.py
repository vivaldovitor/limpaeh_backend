from flask_restful import Api

from resources.LoginResource import LoginResource
from resources.IndexResource import IndexResource
from resources.SolicitacaoResource import SolicitacoesResource, SolicitacaoResource
from resources.RelatoriosResource import RelatoriosResource, RelatorioResource
from resources.FuncionarioResource import FuncionariosResource, FuncionarioResource
from resources.AmbienteResource import AmbientesResource, AmbienteResource
from resources.EmpresaResource import EmpresasResource, EmpresaResource
from resources.TipoFuncionarioResource import TipoUsuariosResource, TipoUsuarioResource
from resources.AtividadeLimpezaResource import AtividadesLimpezaResource, AtividadeLimpezaResource

api = Api()

# Index
api.add_resource(IndexResource, '/')

# Login
api.add_resource(LoginResource, '/login')

# Funcionários
api.add_resource(FuncionariosResource, '/funcionarios')
api.add_resource(FuncionarioResource, '/funcionario/<int:id>')

# Solicitações
api.add_resource(SolicitacoesResource, '/solicitacoes')
api.add_resource(SolicitacaoResource, '/solicitacao/<int:id>')

# Ambientes
api.add_resource(AmbientesResource, '/ambientes')
api.add_resource(AmbienteResource, '/ambiente/<int:id>')

# Empresas
api.add_resource(EmpresasResource, '/empresas')
api.add_resource(EmpresaResource, '/empresa/<int:id>')

# TiposUsuarios
api.add_resource(TipoUsuariosResource, '/tipos_funcionarios')
api.add_resource(TipoUsuarioResource, '/tipo_funcionario/<int:id>')

# AtividadesLimpezas
api.add_resource(AtividadesLimpezaResource, '/atividades_limpeza')
api.add_resource(AtividadeLimpezaResource, '/atividade_limpeza/<int:id>')

# Relatórios
api.add_resource(RelatoriosResource, '/relatorios')
api.add_resource(RelatorioResource, '/relatorio/<int:id>')

# Finalizar atividade
# api.add_resource(FinalizarAtividadeResource, '/finalizar_atividade/<int:id>')