#internal imports
import telebot
import getData
import scheduler
import myToken
#eternal imports
import asyncio
from telebot.async_telebot import AsyncTeleBot

#Chat iD of users to initial tests Rafael:616045077 Group:-871500862 SuperGroup:-1001900572890 Lagoa:5991412323
listOfUsersiD = [-1001900572890]
groupChatiD = -1001900572890

#Objects to store the results
actualResults = {'PTM':[],'PT':[],'PTV':[],'PTN':[],'FED':[],'COR':[]}
receivedResults = {'PTM':[],'PT':[],'PTV':[],'PTN':[],'FED':[],'COR':[]}

#Creating the bot
bot = AsyncTeleBot(myToken.TOKEN)

#Creating a handler to the command /Start of the bot
@bot.message_handler(commands=['Start'])
async def send_welcome(message):
    #Debug print of when an iD connected to the bot
    print(f'iD:{message.chat.id} enviou comando /Start ')
    await bot.reply_to(message, f'Recebi seu comando /Start, estou processando, aguarde por favor...💬')
    await SendResultsToiD(message.chat.id, getData.getResults())

@bot.message_handler(['Teste'])
async def AnwserTest(message: telebot.types.Message):
    await bot.reply_to(message, f'Recebi a sua mensagem de teste')

#Polling in Bot in manual
async def poolingApp(actualResults: dict[str,list]):
    print("Bot iniciou o modo pooling de resultados")
    runCounter = 0
    while True:
        if scheduler.IsNeedStartPooling(15):
            #Search new results on the site
            print("Buscando resultados modo automatico...")
            results = getData.getResults()
            receivedResults = results['tableResult']
            print("Resultados recebidos modo automatico!")

            #Compare previously received results with currently received results
            if actualResults != receivedResults:
                print("Resultados estão diferentes, atualizando...")
                await bot.send_message(groupChatiD,f'O site foi atualizado, vou mandar os resultados 💬')
                #Start sending messages to registered IDs
                for useriD in listOfUsersiD:
                    await SendResultsToiD(useriD, results)
                print("Resultados atualizados e enviados para users cadastrados")
            else:
                print("Resultados não estão diferentes dos anteriores")

            actualResults = receivedResults
            await asyncio.sleep(60)
            runCounter+=1
        await asyncio.sleep(60)
    print(f"Saindo do Loop desativando o Bot que rodou: {runCounter} vezes")

async def SendResultsToiD(useriD, results):
    textResult = ''
    receivedResults = results['tableResult']
    print("Resultados recebidos")
    #Searching the result date
    resultsDate = results['dateResult']
    print(f"Data do resultado enviado: ({resultsDate})")
    await bot.send_message(useriD, f'O resultado que está sendo enviado é de {resultsDate}')
    for resultKeys in receivedResults:
        resultName = resultKeys
        for resultNumber in receivedResults[resultKeys]:
            #Remove the value after the hyphen example: 0389-23
            textResult = textResult + f'{resultNumber.split("-")[0]}, '
        await bot.send_message(useriD, f'{resultName} : {textResult}')
        textResult = ''

#Código principal
async def mainF():
    await asyncio.gather(bot.infinity_polling(),poolingApp(actualResults))

#rodar o código de maneira assincrona
asyncio.run(mainF())