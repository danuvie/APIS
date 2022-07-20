from sql_alchemy import banco


class Site_Model(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80) )
    hoteis = banco.relationship('Hotel_Model') #lista de objetos hoteis
    


    def __init__(self, url):
        self.url = url
       
    
    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis':[hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first() 
        if site:
            return site
        return None

    @classmethod
    def find_site_by_id(cls, site_id):
        site = cls.query.filter_by(site_id=site_id).first() 
        if site:
            return site
        return None


    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    # def update_hotel(self, nome, estrelas, diaria, cidade):
    #     self.nome = nome
    #     self.estrelas = estrelas
    #     self.diaria = diaria
    #     self.cidade = cidade

    def delete_site(self):
        [hotel.delete_hotel() for hotel in self.hoteis]
        banco.session.delete(self)
        banco.session.commit()
