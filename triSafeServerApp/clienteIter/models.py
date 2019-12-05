import requests
import json
from comum.retorno import Retorno

class ClienteIter():
    
    @classmethod
    def tratarRespostaHTTP(cls, respostaHTTP):
        
        retorno = Retorno(True, '', '')
        retorno.dadosJson = respostaHTTP.json()

        if respostaHTTP.status_code < 200 or respostaHTTP.status_code > 300:
            retorno = Retorno(False, respostaHTTP.text, respostaHTTP.status_code)
        
        return retorno

    def obter(self, idCliente):
        token = ClienteIter.autenticarIter(self)
        headers = {'Authorization': 'Bearer %s' %token,
                'Content-Type' : 'application/json' }
        url = "https://cnxs-api.itertelemetria.com/v1/users/{0}".format(idCliente)
        print(url)
        print(headers)
        r = requests.get(url, headers=headers)
        return ClienteIter.tratarRespostaHTTP(r)
        
    # def clientes(request):
    #     return HttpResponse('Olá clientes!')

    # def cliente_por_codigo(request, id):
    #     clientes = listarClientesTriSafeIter(id)

    #     return HttpResponse('Detalhes do cliente: %s' %clientes)

    # def cliente_por_nome(request, nome):
    #     print ("Incluindo cliente")
    #     resposta = incluir(nome)
    #     return HttpResponse('Detalhes do cliente: %s' %resposta)

    def autenticarIter(self):
        headers = {'Authorization': 'Basic ZG9jdW1lbnRhY2FvQGl0ZXIuc2M6ZG9jdW1lbnRhY2FvMTIz'}
        r = requests.get("http://cnxs-api.itertelemetria.com/v1/sign_in", headers=headers)
        
        #TODO:Fazer tratamentos de erro.
        respostaJson = r.json()
        return respostaJson["token"]

    # def listarClientesTriSafeIter(idCliente):
    #     token = autenticarIter()
    #     headers = {'Authorization': 'Bearer %s' %token,
    #                'Content-Type' : 'application/json' }
    #     params = { 'company_id' : idCliente }    
        
    #     r = requests.get("https://cnxs-api.itertelemetria.com/v1/users", headers=headers, params=params)
        
    #     #TODO: Fazer tratamentos de erro.
    #     return r.text

    #TODO: passar para a classe ClienteIter
    def incluir(self, cliente):
        jsonCliente = json.dumps({
            "user": {
                "email": cliente.email,
                "username": cliente.nomeUsuario,
                "name": cliente.nome,
                "document": cliente.cpf,
                "expire_date": "2019-01-01 00:00:00",
                "phone": "99999999999",
                "language": "pt-BR",
                "time_zone": "Brasilia",
                "company_id": 8,
                "password": "superpassword",
                "password_confirmation": "superpassword",
                "access_level": 0,
                "zipcode": "88888888",
                "street": "ttttttt",
                "number": "123",
                "district": "Centro",
                "city": "Porto Alegre",
                "state": "Rio Grande do Sul",
                "active": True
            }
        })

        token = ClienteIter.autenticarIter(self)
        headers = {'Authorization': 'Bearer %s' %token,
                   'Content-Type' : 'application/json' }
        
        r = requests.post("https://cnxs-api.itertelemetria.com/v1/users", headers=headers, data=jsonCliente)
        
        return ClienteIter.tratarRespostaHTTP(r)