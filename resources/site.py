from flask_restful import Resource
from models.site import Site_Model


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in Site_Model.query.all()]}

class Site(Resource):
    def get(self, url):
        site = Site_Model.find_site(url)
        if site:
            return site.json()
        return {'message': 'Site not found'}, 404 # not found

    def post(self, url):
        if Site_Model.find_site(url):
            return {f'message': 'the "{}"site alread exists'}
        site = Site_Model(url)
        try:
            site.save_site()
        except:
            return {'message': 'um erro ocorreu ao tentar criar um novo site'}
        return site.json()


    def delete(self, url):
        site = Site_Model.find_site(url)
        if site:
            site.delete_site()
            return {f'message': 'site "{}" foi deletado'}
        return {'message': 'site not found'}, 404 # site não encontrado