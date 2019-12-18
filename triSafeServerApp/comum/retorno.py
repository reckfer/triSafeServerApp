from django.forms.models import model_to_dict
import json

class Retorno:
    ok = False
    dados = ''
    mensagem = ''
    http_status = ''
    
    def json(self):
        return self.criarJson()
                    
    def __init__(self, estado, msg, http_st):
        
        self.ok = estado
        self.mensagem = msg

        if self.ok:
            if not self.mensagem or len(str(self.mensagem)) <= 0:
                self.mensagem = "OK"
            self.http_status = 200
        else:            
            self.http_status = http_st
        
    def __str__(self):
        return json.dumps(self.criarJson())
        
    def criarJson(self):
        if type(self.dados) == 'dict':
            oDados = model_to_dict(self.dados)
        oDados = self.dados

        ret = {
            "ok": self.ok,
            "dados": oDados,
            "mensagem": self.mensagem,
            "http_status": self.http_status
            }
        return ret