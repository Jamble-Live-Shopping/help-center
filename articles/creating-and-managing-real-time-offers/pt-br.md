# Criar e gerenciar Ofertas em tempo real

## O que você vai aprender

Este guia explica como rodar o modo **Oferta em tempo real** durante o seu show ao vivo na Jamble. Você vai configurar o produto, fixar o item no show, acompanhar as ofertas dos compradores em tempo real e aceitar a oferta vencedora ao final do timer.

## Antes de começar

Você precisa de:

- Uma conta de vendedor aprovada na Jamble
- Um produto adicionado ao seu show com o modo de venda **Oferta em tempo real** selecionado
- O app aberto na tela do show, pronto para entrar ao vivo

## Como funciona o modo Oferta em tempo real

Quando você publica um produto com o modo **Oferta em tempo real**, a venda acontece em formato de disputa por tempo. Durante o show:

1. Você fixa o produto na tela do show
2. Um timer de contagem regressiva começa
3. Os compradores enviam ofertas pelo botão **Oferta** (a maior oferta fica visível para todos)
4. Quando uma oferta chega perto do final, o timer ganha alguns segundos extras
5. Ao acabar o timer sem novas ofertas, a maior oferta vence

A última oferta vence ao final do tempo. Você não precisa aceitar manualmente: o sistema fecha a venda na maior oferta assim que o timer zera.

## Passo a passo

### Passo 1: escolha o modo de venda do produto

Ao adicionar ou editar um produto no seu show, abra a tela **Modo de venda** e selecione **Oferta em tempo real**. Os campos **Comece em** e **Duração (segundos)** aparecem logo abaixo da opção marcada.

![Tela Modo de venda com três opções, Oferta em tempo real selecionado em destaque, e os campos Comece em e Duração (segundos) visíveis abaixo](./assets/mockups/creating-and-managing-real-time-offers__screen-1__pt-br__v3.png)

A tela mostra os três modos disponíveis:

- **Oferta em tempo real**, com timer e disputa em tempo real
- **Morte súbita**, parecida com a Oferta em tempo real, mas **sem prorrogação de tempo**
- **Comprar agora**, preço fixo, sem timer

Defina o **Comece em** (preço inicial, entre R$ 5,00 e R$ 5.000,00) e a **Duração (segundos)** do timer (entre 10 e 90 segundos). O preço inicial funciona como mínimo: as ofertas precisam ser iguais ou maiores que ele.

### Passo 2: ative a Pré-oferta, se quiser (opcional)

Para produtos de **Oferta em tempo real** com quantidade igual a 1, ainda na tela de criação do produto, há o seletor **Ativar Pré-oferta?**. Quando ativo, os compradores podem fazer ofertas antes do show começar.

![Linha Ativar Pré-oferta? com o seletor ativado em roxo, subtítulo As ofertas podem ser feitos antes do início do show](./assets/mockups/creating-and-managing-real-time-offers__screen-3__pt-br__v3.png)

A Pré-oferta cria expectativa e garante que já existe disputa quando você entra ao vivo. As ofertas feitas antes do show são levadas em conta quando o produto é fixado.

### Passo 3: fixe o produto no show

Quando estiver ao vivo, abra a sua lista de produtos pelo ícone de sacola, no canto inferior da tela, e toque em **Fixar** no produto que você quer vender. O item aparece na tela do show para a audiência, mas a venda ainda não começou.

### Passo 4: inicie a venda

Toque no botão **Iniciar Oferta** que aparece no rodapé da barra de venda. O timer começa a contar e a barra passa a mostrar a quantidade de ofertas em tempo real.

![Sobreposição ao vivo do show: rótulo Vendas em tempo real no canto superior esquerdo, card do produto na parte inferior com a foto e o nome do produto à esquerda, o preço da maior oferta R$ 75,00 e o cronômetro compacto (ícone auction_time_icon + 0:18) empilhados à direita do card e o botão roxo 3 ofertas em uma linha separada abaixo](./assets/mockups/creating-and-managing-real-time-offers__screen-2__pt-br__v3.png)

Os elementos visíveis são:

- **Vendas em tempo real**, no canto superior esquerdo, com o valor atual ao lado
- **Cronômetro compacto** (ícone de relógio + tempo restante, no exemplo **0:18**), posicionado logo abaixo do preço da maior oferta, na coluna direita do card. O cronômetro fica em âmbar e muda para vermelho quando está prestes a terminar.
- **Card do produto na parte inferior**, com a foto e o nome do produto à esquerda, o preço atual e o cronômetro empilhados à direita, e o botão roxo **3 ofertas** em uma linha separada logo abaixo (a quantidade atualiza a cada oferta nova)

### Passo 5: acompanhe as ofertas e o timer

Você não precisa fazer nada enquanto o timer está rodando. O sistema atualiza a maior oferta em tempo real e adiciona segundos quando uma oferta chega perto do final. Foque em mostrar o produto na câmera e falar com a audiência.

### Passo 6: aceite a oferta vencedora

Quando o timer chega a zero sem novas ofertas, a venda encerra automaticamente. O botão da barra de venda muda para **Oferta encerrada** e o app anuncia o ganhador na tela do show. Você não precisa confirmar manualmente: o sistema fecha o pedido na maior oferta.

A partir daí, a barra de venda mostra duas ações para o próximo passo:

- **Reiniciar**, para rodar o mesmo produto de novo, útil quando você tem mais unidades ou quando a primeira oferta ficou baixa
- **Próximo item**, para passar para o próximo produto da fila

## Como o timer funciona

O **Comece em** define o preço mínimo da disputa e a **Duração (segundos)** define o tempo inicial. Quando uma oferta é enviada perto do final do timer, alguns segundos extras são adicionados para dar chance de resposta. O timer continua se estendendo enquanto novas ofertas chegam perto do final, e a venda só fecha quando passa o tempo sem nova oferta.

Esse comportamento previne ofertas de última hora e empurra o preço para cima naturalmente. Por isso a duração mínima é curta (10 segundos): a disputa ganha tempo sozinha quando o público está engajado.

## Quando ninguém faz oferta

Se o timer zera sem nenhuma oferta:

- A venda encerra sem ganhador
- O produto sai da tela ativa e fica disponível para você rodar de novo
- Você pode tocar em **Reiniciar** ou voltar para a sua lista de produtos pelo ícone de sacola

Isso é normal. Antes de rodar de novo, vale falar mais do produto na câmera, baixar um pouco o **Comece em** ou apresentar outro item para aquecer a audiência.

## Oferta em tempo real ou Morte súbita

Os dois modos têm disputa por ofertas. A diferença é como o timer reage:

- **Oferta em tempo real**: o timer ganha segundos extras quando uma oferta chega perto do final. Bom para itens raros, onde a disputa pode esticar e puxar o preço para cima
- **Morte súbita**: o timer não ganha tempo extra. Bom para girar estoque rápido e criar urgência (o comprador precisa decidir antes do zero)

Não existe regra: vendedores costumam misturar os dois no mesmo show, **Oferta em tempo real** nos destaques e **Morte súbita** para acelerar o catálogo padrão.

## Dicas para rodar o seu show

- **Apresente o produto antes de iniciar.** Conte a história do item, o estado, por que ele é especial. A audiência precisa estar atenta antes do timer começar
- **Use uma duração curta para criar empolgação.** Entre 15 e 30 segundos costuma funcionar bem, porque o timer se estende sozinho quando aparece oferta
- **Ative Pré-oferta nos itens destaque.** Os compradores já entram disputando, e o show abre com energia
- **Não inicie várias vendas ao mesmo tempo.** Foque a atenção da audiência em um produto por vez

## Perguntas frequentes

**Posso definir um preço mínimo?**
Sim. O **Comece em** é o preço inicial e funciona como mínimo. As ofertas precisam ser iguais ou maiores que esse valor.

**O que acontece se dois compradores enviam o mesmo valor?**
A oferta enviada primeiro ganha. O sistema registra o horário exato de cada oferta.

**Posso encerrar a venda antes do timer?**
Você não controla o timer manualmente. A venda fecha sozinha quando o tempo zera sem nova oferta. Em casos de pagamento não confirmado, o app abre um alerta perguntando se você quer **Reiniciar** o produto.

**Posso usar Pré-oferta em todos os modos?**
Não. A Pré-oferta só fica disponível em **Oferta em tempo real** e **Morte súbita**, sempre com quantidade igual a 1. Os modos **Comprar agora** e Doação não têm esse seletor.

**Quanto dura a Oferta em tempo real?**
Você escolhe. A duração mínima é 10 segundos e a máxima é 90 segundos. O timer pode esticar sozinho quando aparecem ofertas perto do final.

**O comprador paga o frete?**
Sim. O frete é calculado e somado no checkout, como em qualquer compra na Jamble.

## Precisa de ajuda?

Fale com a gente pelo chat do app ou envie um email para support@jambleapp.com.
