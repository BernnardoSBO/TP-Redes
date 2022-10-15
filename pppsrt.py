#################################################################
# pppsrt.py - protocolo ponto-a-ponto simples com retransmissão
#           - entrega interface semelhante a um socket
#################################################################
# fornece a classe PPPSRT, que tem os métodos:
#
# contrutor: pode receber um ou dois parâmetros, para criar um
#            canal que implementa o protocolo PPPSRT;
#            - o servidor cria o objeto apenas com o porto;
#            - o cliente cria o objeto com host e porto.
# close: encerra o enlace
# send(m): envia o array de bytes m pelo canal, calculando o 
#           checksum, fazendo o enquadramento e controlando a
#           retransmissão, se necessário.
# recv(): recebe um quadro e retorna-o como um array de bytes,
#         conferindo o enquadramento, conferindo o checksum e
#         enviando uma mensagem de confirmação, se for o caso.
# OBS: o tamanho da mensagem enviada/recebida pode variar, 
#      mas não deve ser maior que 1500 bytes.
################################################################
# PPPSRT utiliza o módulo dcc023_tp1 como API para envio e recepção
#        pelo enlace; o qual não deve ser alterado.
# PPPSRT não pode utilizar a interface de sockets diretamente.
################################################################

import dcc023_tp1

def onesCompAdd16(num1, num2):
    mod = 1 << 16
    result = num1+num2
    return result if result < mod else (result+1) % mod


class PPPSRT:
  
    def __init__(self, port, host='' ):
        self.link = dcc023_tp1.Link(port,host)

    def close(self):
        self.link.close()
        
####################################################################
# A princípio, só é preciso alterar as duas funções a seguir.

    def sumAll16Bytes(self, byteList):
        total = 0
        #para cada item na lista de palavras de 2bytes, somar em
        #complemento de 1 ao total
        for i in byteList:
            total = onesCompAdd16(total, int.from_bytes(i, 'big'))

        #retornando o checkSum
        return total.to_bytes(2, 'big')

    def checkSum(self, message):
        #separando palavras com 2bytes de tamanho
        splittedMessage = [message[i:i+2] for i in range(0,len(message),2)]

        
        #calculando soma em complemento de 1 das palavras de 2bytes: checksum
        checksum = self.sumAll16Bytes(splittedMessage)
        
        #anexando checksum de 2 bytes no final do pacote
        message = message + checksum

        #retornando o pacote
        return message

    def framming(self, message, isFrame:bool):

        if isFrame:
            message = self.protocol(True, message)
            message = self.controlFrame(message)
            message = self.address(message)
            message = self.checkSum(message)
            message = self.flagging(message)

        #else: #is Ack
            

        return message

    def protocol(self, bool: bool, message):

        if bool:
            frameNumber = (1).to_bytes(2, 'big')
        else: 
            frameNumber = (0).to_bytes(2, 'big')

        print('frameNumber:', frameNumber)
        message = frameNumber + message
        return message

    def flagging(self, message):
        flag = bytes([0x7e])
        print('flag:', flag)
        flaggedMessage = flag + message + flag
        return flaggedMessage

    def controlFrame(self, message):
        controlByte = bytes([0x03])
        print('controlByte:', controlByte)
        message = controlByte + message
        return message

    def address(self, message):
        addressByte = bytes([0xff])
        print('address byte:',addressByte)
        message = addressByte + message
        return message

    def send(self,message):
        # Aqui, PPSRT deve fazer:
        #   - fazer o encapsulamento de cada mensagem em um quadro PPP,
        #   - calcular o Checksum do quadro e incluído,
        message = self.framming(message, True)
        #   - fazer o byte stuffing durante o envio da mensagem,
        message = [message[i:i+1] for i in range(len(message))]

        for i in range(len(message)):
            if i==
        #   - aguardar pela mensagem de confirmação,
        #   - retransmitir a mensagem se a confirmação não chegar.
        
        self.link.send(message[0])
    
    def recv(self):
        # Aqui, PPSRT deve fazer:
        #   - identificar começo de um quadro,
        #   - receber a mensagem byte-a-byte, para retirar o stuffing,
        #   - detectar o fim do quadro,
        #   - calcular o checksum do quadro recebido,
        #   - descartar silenciosamente quadros com erro,
        #   - enviar uma confirmação para quadros recebidos corretamente,
        #   - conferir a ordem dos quadros e descartar quadros repetidos.
        try:
            frame = self.link.recv(1500)
        except TimeoutError: # use para tratar temporizações
            print("Timeout")
        return frame



#   8       8         8         16         _        16        8
# flag | address | control | protocol | payload | checksum | flag
#   
#   flag =      01111110 (0x7E) -> flag de inicio e final de quadro
#   address =   11111111 (0xFF) -> como é ponto a ponto, vamos usar esse valor fixo
#   control
#      -frame = 00000011 (0x03)
#      -ack   = 00000111 (0x07)
#   protocol = numerate frames and acks
#   payload = max(1500 bytes)
#   byte stuffing = 01111101 (0x7d)
#       - when escaping, change to 0x7d followed by 0x5_
#               . 0x5d to escape a escape  -> 0x7d 0x5d
#               . 0x5e to escape a flag    -> 0x7d 0x5e
#
#   when ack, | payload | == 0

###############################################################
#
#   PACKET
#
#                                         DATA
#                              PROTOCOL | DATA
#                    CONTROL | PROTOCOL | DATA
#          ADDRESS | CONTROL | PROTOCOL | DATA
#
###############################################################
#
#   FRAME
#
#          ADDRESS | CONTROL | PROTOCOL | DATA | CHECKSUM
#   FLAG | ADDRESS | CONTROL | PROTOCOL | DATA | CHECKSUM | FLAG
#
###############################################################

# ENVIO BYTE A BYTE
#
#
#
# TIME OUT EM RECV É PARA RECEBER ACK!!!!!


# AO RECEBER, CHECAR SE JÁ RECEBEU O PACOTE

# ENQUADRAMENTO VAI FAZENDO O BYTE STUFFING ENQUANTO VAI MANDANDO BYTE A BYTE


