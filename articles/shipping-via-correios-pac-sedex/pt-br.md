# Envio via Correios (PAC/SEDEX)

## O que você vai aprender

Este guia explica como o envio funciona na Jamble para vendedores brasileiros. Você vai aprender sobre as transportadoras disponíveis, como os custos de frete são calculados, como as etiquetas são geradas e o que esperar ao longo do processo de envio.

## Antes de começar

- Você precisa de uma conta de vendedor aprovada na Jamble
- Você precisa de um endereço de envio cadastrado nas suas configurações
- Você precisa de pelo menos uma venda concluída para enviar

## Como o envio funciona na Jamble

Quando um comprador adquire um produto durante seu show ao vivo, a Jamble cuida da logística de envio para você. Veja o fluxo:

1. **A venda acontece** durante seu show
2. **A Jamble calcula** o custo de envio com base no peso/tamanho do item e na distância entre seu endereço e o do comprador
3. **Uma etiqueta de envio** é gerada automaticamente
4. **Você embala e envia** o item usando a etiqueta fornecida
5. **Atualizações de rastreamento** são enviadas para você e para o comprador

Você não precisa ir a uma agência dos Correios para negociar preços ou comprar etiquetas. A Jamble faz isso através do **Melhor Envio**, uma plataforma de logística que se conecta diretamente com as transportadoras para obter as melhores tarifas.

## Transportadoras disponíveis

A Jamble atualmente usa duas transportadoras no Brasil:

| Transportadora | Serviço | Velocidade | Melhor para |
|----------------|---------|------------|-------------|
| **Correios** | PAC | Padrão (mais demorado) | Envio econômico para a maioria dos itens |
| **Correios** | SEDEX | Prioritário (mais rápido) | Entregas urgentes ou com prazo curto |
| **Loggi** | Padrão | Varia por região | Transportadora alternativa, disponível em algumas áreas |

Quando uma etiqueta é gerada, a Jamble seleciona automaticamente entre **dois níveis**:

- **Mais barato**: geralmente PAC (Correios padrão), custo menor, prazo de entrega maior
- **Prioritário**: geralmente SEDEX (Correios expresso), entrega mais rápida, custo maior

O comprador vê as duas opções com prazos estimados e preços antes de finalizar a compra.

![Tela de escolha de forma de envio com PAC (Mais barato, R$ 15,00) selecionado e SEDEX (Prioritário, R$ 25,00) disponível](./assets/mockups/shipping-via-correios-pac-sedex__correios-method-picker__pt-br.png)

## Como os custos de frete são calculados

Os custos de envio são calculados usando **cotações reais de CEP a CEP**, ou seja, a distância exata entre seu código postal e o do comprador. Isso é feito através da API do Melhor Envio.

O custo depende de:

- **Peso do item**, determinado pelo perfil de envio que você escolheu ao listar o produto
- **Dimensões do pacote**, tamanhos padrão baseados no perfil de envio
- **Distância**, do seu endereço de envio até o endereço do comprador

O comprador paga o custo de envio no checkout. Você não é cobrado pelo envio, a menos que opte por cobri-lo.

## Perfis de envio e peso

Quando você lista um produto, escolhe um **perfil de envio** que representa seu peso aproximado. Esses perfis determinam o custo de envio:

| Perfil | Faixa de peso |
|--------|--------------|
| Card | Até ~23g |
| Booster | ~23g a 45g |
| Light Accessories | ~45g a 180g |
| Light Apparel | ~180g a 320g |
| Standard Apparel | ~320g a 680g |
| Heavier Apparel | ~680g a 1,36kg |
| Bulkier Items | ~1,36kg a 2,27kg |
| Small Bundles | ~2,27kg a 3,18kg |
| Medium Bundles | ~3,18kg a 4,54kg |
| Large Bundles | ~4,54kg a 6,80kg |
| Extra-Large Bundles | ~6,80kg a 9,07kg |

**Escolha com precisão.** Se você escolher um perfil leve demais, o pacote pode ser recusado ou cobrado a mais na agência dos Correios. Se for pesado demais, o comprador paga mais do que o necessário.

## Etiquetas de envio

### Formatos de etiqueta

Você pode gerar sua etiqueta de envio em três formatos:

| Formato | Melhor para |
|---------|-------------|
| **Half page PDF** | Impressora doméstica padrão (imprime em meia folha A4) |
| **Thermal PDF (4x6)** | Impressora térmica de etiquetas (se você tiver uma) |
| **Full page PDF** | Folha A4 inteira (uma etiqueta por página) |

### Como gerar uma etiqueta

Depois que uma venda é concluída:

1. Vá para **Settings** → **Minhas vendas**
2. Encontre o pedido que você precisa enviar
3. Toque para abrir os detalhes do pedido
4. A etiqueta de envio estará disponível para download ou impressão

A Jamble gera a etiqueta automaticamente com todas as informações da transportadora, número de rastreamento e endereços preenchidos.

![Tela de detalhes da venda com aviso "Envie o pacote rapidamente", cartão do pedido e botão Baixar etiqueta de envio](./assets/mockups/shipping-via-correios-pac-sedex__drop-off-reminder__pt-br.png)

### Embalando e despachando

Uma vez que você tenha sua etiqueta:

1. **Embale o item com segurança**, use embalagem apropriada para o tipo de produto
2. **Cole a etiqueta**, imprima e fixe firmemente na parte externa do pacote
3. **Leve a uma agência** dos Correios ou ponto de coleta autorizado

Você pode encontrar a agência dos Correios mais próxima pelo site ou app dos Correios.

## Rastreando seu envio

Uma vez que o pacote é escaneado pela transportadora, as atualizações de rastreamento ficam disponíveis para você e para o comprador. Os status de rastreamento incluem:

| Status | O que significa |
|--------|----------------|
| **Pré-postagem** | Etiqueta criada, pacote ainda não escaneado |
| **Em trânsito** | Pacote a caminho |
| **Entregue** | Pacote entregue ao comprador |
| **Devolvido** | Pacote devolvido para você |

Tanto você quanto o comprador recebem notificações push sobre atualizações de rastreamento (se a notificação **"Updates on transaction status"** estiver habilitada).

![Tela de rastreamento com Correios SEDEX, número de rastreamento BR123456789BR e linha do tempo mostrando Etiqueta criada, Postado nos Correios, Em trânsito e Entregue](./assets/mockups/shipping-via-correios-pac-sedex__correios-tracking__pt-br.png)

## Dicas importantes

- **Envie rapidamente.** Compradores esperam envio rápido. Tente despachar seus pacotes em 1 a 2 dias úteis após a venda
- **Verifique o peso antes de listar.** Se você não tem certeza do peso de um produto, use uma balança de cozinha. Escolher o perfil de envio errado causa problemas para você e para o comprador
- **Mantenha seu endereço de envio atualizado.** Sua etiqueta é gerada a partir do endereço nas suas configurações. Se você mudar de endereço, atualize imediatamente em **Settings** → **Shipping Preferences**
- **Guarde seu número de rastreamento.** Se um comprador entrar em contato sobre o envio, você vai precisar do número de rastreamento. Ele está disponível no seu histórico de vendas
- **Embale com cuidado.** Itens danificados levam a devoluções e avaliações negativas. Use plástico bolha ou proteção para itens frágeis

## Perguntas frequentes

**Quem paga o frete?**
O comprador paga o custo de envio no checkout. O custo é calculado com base no peso/tamanho do item e na distância entre você e o comprador.

**Posso oferecer frete grátis?**
Isso depende das configurações do show. Algumas promoções ou funcionalidades podem permitir frete grátis para compradores. Entre em contato com o suporte para saber as opções atuais.

**E se o pacote for recusado na agência dos Correios?**
Isso geralmente acontece quando o pacote excede o peso ou as dimensões do perfil de envio. Reembale o item ou entre em contato com o suporte para ajustar a etiqueta.

**Quanto tempo leva o PAC vs SEDEX?**
O PAC (padrão) geralmente leva de 5 a 15 dias úteis dependendo da distância. O SEDEX (prioritário) leva de 1 a 5 dias úteis. Os prazos de entrega variam por região.

**E se o comprador der o endereço errado?**
Se o pacote for devolvido para você por causa de um endereço errado, entre em contato com o suporte. Eles vão ajudar a coordenar com o comprador para obter o endereço correto.

**Posso usar minhas próprias etiquetas dos Correios?**
A Jamble gera etiquetas pelo Melhor Envio. Usar suas próprias etiquetas não é recomendado pois isso ignora a integração de rastreamento.

**O que acontece se o pacote for extraviado?**
Entre em contato com o suporte da Jamble. O envio pelo Melhor Envio inclui rastreamento, e pacotes extraviados são tratados pelo processo de reclamação da plataforma.

## Precisa de ajuda?

Entre em contato pelo chat do app ou envie um email para support@jambleapp.com.
