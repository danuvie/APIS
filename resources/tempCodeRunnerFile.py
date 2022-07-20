from flask_restful import Resource, reqparse
from models.hotel import Hotel_Model


hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'alpha Hotel',
        'estrelas': 4.3,
        'diaria': 400.50,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'beta',
        'nome': 'beta Hotel',
        'estrelas': 3.3,
        'diaria': 300.50,
        'cidade': 'Petrópolis'
    },
    {
        'hotel_id': 'gama',
        'nome': 'gama Hotel',
        'estrelas': 5.0,
        'diaria': 600.50,
        'cidade': 'Arraial do Cabo'
    }
]

 

class Hoteis(Resource):
    def get(self):
        return{"hoteis": hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')


    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'hotel não encontrado'}, 404 # not found
    
    def post(self, hotel_id):
        if Hotel_Model.find_hotel(hotel_id):
            return {f' message: hotel_id {hotel_id} already exists.' }, 400 # bad request

        dados = Hotel.argumentos.parse_args()
        hotel = Hotel_Model(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()
        
        
        



    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_objeto = Hotel_Model(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return hotel, 200 # Atualizado
        hoteis.append(novo_hotel)
        return novo_hotel, 201 # Criado
       

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'hotel deleted'}