from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from Blacklist import BLACKLIST


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='Campo Login obrigatório')
atributos.add_argument('senha', type=str, required=True, help='campo Senha Obrigatório')


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuario não encontrado'}, 404 # not found
    

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'Um erro aconeceu ao tentar salvar'},500 # Internal server error
            user.delete_user()
            return {f'message': 'Usuário foi deletado.' }, 201 # Deletado
        return {'message': "Usuário não encontrado"}


class UserRegister(Resource):
    # /cadastro
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message':'The login "{}" already exits.'.format(dados['login'])}
        
        user = UserModel(dados['login'], dados['senha'])
        user.save_user()
        return {'message': 'user created sucessfully'}, 201 # criado


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'acess_token': token_de_acesso}, 200
        return {'message': 'The username or password does not exist or ir incorrct'}, 401 #unauthorized


class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti'] #JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return{'message': 'Deslogado com sucesso'}

