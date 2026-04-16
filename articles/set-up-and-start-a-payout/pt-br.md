# Configurar e Iniciar um Saque

## O que você vai aprender

Este guia explica como registrar seus dados bancários e sacar seus ganhos da Jamble para sua conta bancária via PIX.

## Antes de começar

Você precisa de:
- Uma conta de vendedor aprovada na Jamble
- Uma conta bancária brasileira no seu nome
- Seu CPF (ou CNPJ se você vende como empresa)
- Ganhos disponíveis na sua carteira (pelo menos uma venda concluída)

## Passo a passo

### Passo 1: Abra sua carteira

Vá ao seu perfil, depois toque em **Settings**. Encontre e toque em **My Wallet**.

```
┌─────────────────────────────────┐
│  Settings                       │
│                                 │
│  SELL                           │
│  My Sales                       │
│  ▶ My Wallet                    │
│  Shipping Preferences           │
│                                 │
└─────────────────────────────────┘
```

Você também pode acessar sua carteira diretamente da sua página de perfil.

### Passo 2: Registre seu banco (somente na primeira vez)

Se é sua primeira vez, você verá um botão **Register Bank** na parte inferior da tela da carteira. Toque nele.

```
┌─────────────────────────────────┐
│  My Wallet                      │
│                                 │
│  [Seções da carteira...]        │
│                                 │
│  ┌───────────────────────────┐  │
│  │      Register Bank        │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

Um alerta aparece:

```
┌─────────────────────────────────┐
│  Registration                   │
│                                 │
│  You must first verify your     │
│  identity and bank details.     │
│  Jamble is powered by Pagar.me  │
│  for more secure transactions   │
│                                 │
│  [ Individual ]                 │
│  [ Company ]                    │
│  [ Later ]                      │
└─────────────────────────────────┘
```

Escolha a opção que corresponde à sua situação:
- **Individual** — se você vende como pessoa física (usando seu CPF)
- **Company** — se você vende como empresa registrada (usando seu CNPJ)

Isso abre um formulário de registro onde você informará seus dados de identidade e bancários. O formulário é fornecido pela **Pagar.me**, parceira de pagamentos da Jamble. Siga os passos do formulário para completar seu registro.

### Passo 3: Verifique seus dados bancários

Após o registro, sua tela da carteira mostra suas informações bancárias em uma seção **Bank Details** na parte inferior.

```
┌─────────────────────────────────┐
│  My Wallet                      │
│                                 │
│  [Seções de saldo]              │
│                                 │
│  ┌───────────────────────────┐  │
│  │ Bank Details              │  │
│  │ Banco XXX - Ag XXXX      │  │
│  │ CC XXXXX-X        [Update]│  │
│  └───────────────────────────┘  │
│                                 │
│  ┌───────────────────────────┐  │
│  │       Withdraw            │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

Se precisar mudar seus dados bancários, toque no botão **Update** ao lado das informações do banco.

### Passo 4: Saque seus ganhos

Quando tiver ganhos disponíveis na sua carteira, o botão **Withdraw** aparece na parte inferior da tela. Toque nele para solicitar um saque.

Pronto — um toque só. A Jamble envia seu saldo disponível para sua conta bancária registrada via transferência bancária. O valor mínimo de saque é **R$ 100**. Transferências geralmente levam de **2 a 5 dias úteis** para chegar.

**Atenção:** Você só pode sacar uma vez a cada 24 horas. Após um saque, o botão mostrará uma contagem regressiva até o próximo saque estar disponível.

### Passo 5: Acompanhe seu saque

Após solicitar um saque, você pode acompanhar o progresso. Toque no **ícone de relógio** no canto superior direito da tela da carteira para abrir o **Payouts History**.

```
┌─────────────────────────────────┐
│  Payouts History                │
│                                 │
│  #PAY-12345        R$ 350,00   │
│  Completed         19/03/2026   │
│  ─────────────────────────────  │
│  #PAY-12340        R$ 520,00   │
│  Processing        18/03/2026   │
│  ─────────────────────────────  │
│  #PAY-12335        R$ 180,00   │
│  Failed            17/03/2026   │
│                                 │
└─────────────────────────────────┘
```

Cada saque mostra:
- **ID do saque** — um número de referência único
- **Valor** — quanto foi sacado
- **Status** — onde o saque está no processo
- **Data** — quando o saque foi solicitado

### Status dos saques

| Status | O que significa |
|--------|----------------|
| Created | Sua solicitação de saque foi recebida |
| Processing | A Pagar.me está processando a transferência para seu banco |
| Pending | A transferência está aguardando para ser concluída |
| Completed | O dinheiro chegou na sua conta bancária |
| Failed | Algo deu errado (veja o artigo de resolução de problemas) |
| Canceled | O saque foi cancelado |

## Dicas importantes

- **Registre seu banco ANTES da primeira venda.** Não espere até ter ganhos — configure seus dados bancários cedo para que os saques sejam instantâneos quando precisar
- **Saque é um toque só.** Toque em "Withdraw" e todo seu saldo disponível é enviado para seu banco. Valor mínimo de saque é R$ 100
- **Transferências levam 2-5 dias úteis.** Após solicitar um saque, a transferência bancária geralmente chega dentro de 2 a 5 dias úteis. Confira o "Payouts History" para acompanhar
- **Um saque por dia.** Você pode sacar uma vez a cada 24 horas. Planeje seus saques
- **Mantenha seus dados bancários atualizados.** Se mudar de banco, atualize seus dados na carteira antes de solicitar um saque. Saques para dados bancários incorretos vão falhar
- **Individual vs Company importa.** Escolha o tipo correto durante o registro. Se você é uma empresa registrada (MEI, LTDA, etc.), selecione "Company" para usar seu CNPJ. Caso contrário, selecione "Individual" para seu CPF

## Perguntas frequentes

**Como recebo meu dinheiro?**
Via PIX. Quando você toca em "Withdraw", a Jamble transfere seu saldo disponível para sua conta bancária registrada usando PIX.

**Quanto tempo um saque demora?**
Transferências bancárias geralmente levam de 2 a 5 dias úteis para chegar na sua conta.

**Tem um valor mínimo de saque?**
Sim. O valor mínimo de saque é R$ 100. Seu saldo disponível precisa ser de pelo menos R$ 100 para ver o botão Withdraw.

**Com que frequência posso sacar?**
Uma vez a cada 24 horas. Após um saque, você precisará esperar 24 horas antes de poder sacar novamente.

**Posso sacar para qualquer banco?**
Você pode sacar para qualquer conta bancária brasileira que aceite PIX e esteja registrada no seu nome (correspondendo ao seu CPF ou CNPJ).

**Não vejo o botão Withdraw. Por quê?**
Ou você ainda não tem ganhos disponíveis (seus pedidos podem ainda estar em andamento), ou não registrou seus dados bancários. Veja se o botão diz "Register Bank" — se sim, complete o registro bancário primeiro.

**Posso mudar minha conta bancária?**
Sim. Toque no botão **Update** na seção Bank Details da sua carteira para atualizar suas informações bancárias.

**E se meu saque falhar?**
Confira se seus dados bancários estão corretos. A causa mais comum de saques falhados é informação bancária incorreta. Atualize seus dados e tente novamente. Se o problema persistir, entre em contato com o suporte.

## Precisa de ajuda?

Entre em contato pelo chat do app ou envie um email para support@jambleapp.com.
