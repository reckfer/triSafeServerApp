import json

class Retorno:
    ok = False
    dadosJson = None
    dados = ''
    mensagem = ''
    http_status = ''
    
    def json(self):
        if self.ok and self.dadosJson is not None:
            return self.dadosJson
            
        return { "ok": self.ok, "mensagem": self.mensagem }
                    
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
        if self.ok and self.dadosJson:
            return str(self.dadosJson)

        return "%s - %s" % (self.http_status, self.mensagem)