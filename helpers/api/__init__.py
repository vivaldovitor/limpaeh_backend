from flask_restful import Api

from resources.LoginResource import LoginResource
from resources.IndexResource import IndexResource
from resources.RelatoriosResource import RelatoriosResource, RelatorioResource
from resources.UsuarioResource import UsuariosResource, UsuarioResource
from resources.AmbienteResource import AmbientesResource, AmbienteResource
from resources.ContratoResource import ContratosResource, ContratoResource
from resources.EmpresaResource import EmpresasResource, EmpresaResource
from resources.TipoUsuarioResource import TipoUsuariosResource, TipoUsuarioResource
from resources.AtividadeLimpezaResource import AtividadesLimpezaResource, AtividadeLimpezaResource
from resources.FuncionarioContratoResource import FuncionariosContratoResource, FuncionarioContratoResource

api = Api()

# Index
api.add_resource(IndexResource, '/')

# Login
api.add_resource(LoginResource, '/login')

# Usuários
api.add_resource(UsuariosResource, '/usuarios')
api.add_resource(UsuarioResource, '/usuario/<int:id>')


# Ambientes
api.add_resource(AmbientesResource, '/ambientes')
api.add_resource(AmbienteResource, '/ambiente/<int:id>')


# Contratos
api.add_resource(ContratosResource, '/contratos')
api.add_resource(ContratoResource, '/contrato/<int:id>')


# Empresas
api.add_resource(EmpresasResource, '/empresas')
api.add_resource(EmpresaResource, '/empresa/<int:id>')


# TiposUsuarios
api.add_resource(TipoUsuariosResource, '/tipos_usuarios')
api.add_resource(TipoUsuarioResource, '/tipo_usuario/<int:id>')


# AtividadesLimepezas
api.add_resource(AtividadesLimpezaResource, '/atividades_limpeza')
api.add_resource(AtividadeLimpezaResource, '/atividade_limpeza/<int:id>;')


# FuncionariosContratosResource
api.add_resource(FuncionariosContratoResource, '/funcionarios_contratos')
api.add_resource(FuncionarioContratoResource, '/funcionario_contrato/<int:id>')


# Relatórios
api.add_resource(RelatoriosResource, '/relatorios')
api.add_resource(RelatorioResource, '/relatorio/<int:id>')
