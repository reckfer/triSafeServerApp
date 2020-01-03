from django.forms.models import model_to_dict
import json

class Retorno:
                        
    def __init__(self, ind_ok = False, msg = '', codMensagem = '', httpStatus = 500):        
        self.estado = EstadoExecucao(ind_ok, msg, codMensagem, httpStatus)
        self.dados = ''

    def json(self):
        return self.__criarJson__()

    def __criarJson__(self):
        if type(self.dados) == 'dict':
            oDados = model_to_dict(self.dados)
        oDados = self.dados

        ret = {
            "estado": self.estado.json(),
            "dados": oDados,
            }
        return ret
    
    def __str__(self):
        return json.dumps(self.__criarJson__())

class EstadoExecucao:
    def __init__(self, indOK = False, msg = '', codMensagem = '', httpStatus = 500):
        
        self.ok = indOK
        self.mensagem = msg
        self.codMensagem = codMensagem

        if self.ok:            
            self.httpStatus = 200
        else:            
            self.httpStatus = httpStatus
        
    def json(self):
        return self.__criarJson__()

    def __criarJson__(self):
        ret = {
            "ok": self.ok,
            "mensagem": self.mensagem,
            "cod_mensagem": self.codMensagem,
            "http_status": self.httpStatus
            }
        return ret

    def __str__(self):
        return json.dumps(self.__criarJson__())