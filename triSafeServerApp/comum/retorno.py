import json

class Retorno:
    ok = False
    dadosJson = None
    dados = ''
    mensagem = ''
    http_status = ''
    
    def json(self):
        if self.dadosJson is not None:
            return self.dadosJson
            
        return { "ok": self.ok, "mensagem": self.mensagem }
                    
    def __init__(self, estado, msg, http_st):
        self.ok = estado
        print(self.ok)
        if self.ok:
            self.mensagem = "OK"
            self.http_status = 200    
        else:
            self.mensagem = msg
            self.http_status = http_st
        
    def __str__(self):
        return "%s - %s" % (self.http_status, self.mensagem)