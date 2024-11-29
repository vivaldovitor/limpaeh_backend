from flask_restful import Api

from resources.IndexResource import IndexResource
from resources.UsuarioResource import UsuariosResource
from resources.AmbienteResource import AmbientesResource
from resources.ContratoResource import ContratosResource
from resources.EmpresaResource import EmpresasResource
from resources.TipoUsuarioResource import TipoUsuarioResource
from resources.AtividadeLimpezaResource import AtividadesLimpezaResource


api = Api()

# Index
api.add_resource(IndexResource, '/')

# Usuários
api.add_resource(UsuariosResource, '/usuarios')

# Ambientes
api.add_resource(AmbientesResource, '/ambientes')

# Contratos
api.add_resource(ContratosResource, '/contratos')

# Empresas
api.add_resource(EmpresasResource, '/empresas')

# TiposUsuarios
api.add_resource(TipoUsuarioResource, '/tipos_usuarios')

# AtividadesLimepezas
api.add_resource(AtividadesLimpezaResource, '/atividades_limpeza')
