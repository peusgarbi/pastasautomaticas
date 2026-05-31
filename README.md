# Gerador Automático de Pastas

Sistema para geração automática de receitas de alta, atestados médicos e declarações de acompanhante a partir da agenda cirúrgica em PDF.

- Gera pastas de alta com receita e orientações automáticas para os pacientes cirúrgicos do HIORP;
- Faz a **felicidade** dos residentes.

> By [Peusgarb.](https://github.com/peusgarbi) :sunglasses:

## Índice

* [Obtendo a Agenda Cirúrgica](#obtendo-a-agenda-cirúrgica)
* [Gerando os Documentos](#gerando-os-documentos)
* [Arquivos Gerados](#arquivos-gerados)
* [Limpar Impressos](#limpar-impressos)
* [Configuração das Receitas](#configuração-das-receitas)
* [Criando uma Nova Receita](#criando-uma-nova-receita)
* [Primeira Utilização](#primeira-utilização)
* [Cadastro de Cirurgiões](#cadastro-de-cirurgiões)
* [Editar um Cirurgião](#editar-um-cirurgião)
* [Excluir um Cirurgião](#excluir-um-cirurgião)
* [Problemas Comuns](#problemas-comuns)

## Obtendo a Agenda Cirúrgica

Antes de utilizar o programa, é necessário exportar a agenda cirúrgica do dia em formato PDF.

1. Acesse o sistema **HiperDoctor** utilizando seu usuário e senha.
1. Abra o módulo **Agenda Cirúrgica**.
1. Clique em **Impressos**.
1. Selecione o relatório: `Relatório Farmácia Novo`
1. Gere o relatório e salve o arquivo PDF em seu computador.
1. No Gerador de Receitas, clique em **Selecionar PDF** e escolha o arquivo salvo.

> [!WARNING]
> Atenção: o sistema foi desenvolvido para processar o relatório "Relatório Farmácia Novo". Outros relatórios podem não ser reconhecidos corretamente.

## Gerando os Documentos

### 1. Selecionar a Agenda

Clique em **Selecionar PDF** e escolha a agenda cirúrgica do dia.

### 2. Gerar os Documentos

Clique em **Gerar Documentos**.

O sistema irá:

* Ler a agenda cirúrgica
* Identificar os pacientes
* Localizar os modelos de receita correspondentes
* Gerar receitas de alta
* Gerar atestados médicos
* Gerar declarações para acompanhantes

## Arquivos Gerados

Todos os documentos são salvos na pasta:

```text
impressos/
```

Será também gerado um arquivo com todos os documentos consolidados em um só para facilitar a impressão:

```text
impressos/RECEITAS CONSOLIDADAS.docx
```

Exemplo:

```text
impressos/
├── MARIA - RECEITA ALTA.docx
├── MARIA - ATESTADO.docx
├── MARIA - DECLARACAO ACOMPANHANTE.docx
├── JOAO - RECEITA ALTA.docx
├── JOAO - ATESTADO.docx
├── RECEITAS CONSOLIDADAS.docx
└── ...
```

## Limpar Impressos

O botão **Limpar Impressos** remove todos os arquivos da pasta `impressos`.

Utilize esta opção antes de iniciar um novo dia de trabalho.

> [!WARNING]
> Atenção: esta ação não pode ser desfeita.

## Configuração das Receitas

O sistema utiliza arquivos de texto (`.txt`) para montar automaticamente as receitas de alta.

Cada combinação de procedimentos deve possuir um arquivo correspondente.

> [!IMPORTANT]
> Atenção: o nome dos procedimentos precisa estar escrito por extenso e da mesma forma como cadastrado no relatório do mapa cirúrgico.

### Estrutura de Pastas

```text
receitas/
├── PEDRO SGARBI/
│   ├── ADULTO/
│   │   ├── ADENOIDECTOMIA.txt
│   │   ├── SEPTOPLASTIA+TURBINECTOMIA BILATERAL.txt
│   │   └── ...
│   └── CRIANCA/
│       ├── ADENO - AMIGDALECTOMIA+TURBINECTOMIA BILATERAL.txt
│       └── ...
├── FULANA DE TAL/
│   ├── ADULTO/
│   └── CRIANCA/
└── ...
```

### Nome das Pastas

A pasta do médico deve possuir exatamente o mesmo nome cadastrado no sistema e que aparece no relatório do mapa cirúrgico.

Exemplo:

```text
PEDRO SGARBI
```

### Pastas Obrigatórias

Dentro da pasta de cada médico devem existir duas subpastas:

```text
ADULTO
CRIANCA
```

### Nome dos Arquivos

O nome do arquivo deve corresponder exatamente aos procedimentos realizados.

Quando houver mais de um procedimento, os nomes devem ser separados apenas pelo caractere:

`+`

Exemplos:

```text
ADENOIDECTOMIA.txt
SEPTOPLASTIA+TURBINECTOMIA BILATERAL.txt
ADENO - AMIGDALECTOMIA+TURBINECTOMIA BILATERAL.txt
```

> [!IMPORTANT]
> Importante: os procedimentos devem estar em ordem alfabética.

### Conteúdo dos Arquivos

Os arquivos devem conter apenas os medicamentos e orientações da receita.

Exemplo:

```text
Via Oral

1. AMOXICILINA + CLAVULANATO 400+57MG/5ML
Tomar _____ mL, de 12/12 horas, por 7 dias

2. PREDNISOLONA 3MG/ML
Tomar _____ mL, de 12/12 horas, por 5 dias

3. DIPIRONA GOTAS
Tomar _____ gotas, de 6/6 horas, se dor ou febre

Via Nasal

4. SORO FISIOLÓGICO 0,9%
Realizar lavagem nasal de 4/4 horas
```

Não é necessário incluir:

* Nome do paciente
* Endereço
* Data
* Nome do médico
* CRM
* RQE

Essas informações são adicionadas automaticamente pelo sistema durante a geração do documento.

### Como o Sistema Escolhe a Receita

O sistema identifica:

1. O cirurgião responsável.
1. Se o paciente é adulto ou criança.
1. Os procedimentos realizados.

Com essas informações, procura automaticamente o arquivo correspondente dentro da estrutura de pastas.

Caso o arquivo não seja encontrado, a receita daquele paciente não será gerada e uma mensagem será exibida no log do programa.

## Criando uma Nova Receita

Sempre que surgir uma nova combinação de procedimentos, será necessário criar um novo arquivo de receita.

### Passo 1: Identificar os Procedimentos

Verifique na agenda cirúrgica quais procedimentos foram realizados.

Exemplo:

```text
SEPTOPLASTIA + TURBINECTOMIA BILATERAL + ADENOIDECTOMIA
```

### Passo 2: Ordenar os Procedimentos

Os procedimentos devem ser organizados em ordem alfabética.

Exemplo:

```text
ADENOIDECTOMIA + SEPTOPLASTIA + TURBINECTOMIA BILATERAL
```

### Passo 3: Montar o Nome do Arquivo

Junte os procedimentos utilizando apenas o caractere `+` e remova os espaços.

Resultado:

```text
ADENOIDECTOMIA+SEPTOPLASTIA+TURBINECTOMIA BILATERAL.txt
```

### Passo 4: Escolher a Pasta Correta

Identifique:

* O cirurgião responsável.
* Se a receita é para adulto ou criança.

Exemplo:

```text
receitas/
└── PEDRO SGARBI/
    └── CRIANCA/
        └── ADENOIDECTOMIA+SEPTOPLASTIA+TURBINECTOMIA BILATERAL.txt
```

### Passo 5: Criar o Arquivo

Caso o arquivo ainda não exista:

1. Copie uma receita semelhante.
1. Renomeie o arquivo.
1. Ajuste os medicamentos conforme necessário.

### Dicas

#### Reaproveite Modelos Existentes

Na maioria dos casos, é mais rápido copiar uma receita semelhante e apenas ajustar os medicamentos.

#### Atenção ao Nome do Arquivo

O sistema procura o arquivo utilizando exatamente o nome dos procedimentos identificados na agenda cirúrgica.

Diferenças de escrita podem impedir a localização do modelo.

Exemplos incorretos:

```text
ADENOIDECTOMIA + AMIGDALECTOMIA.txt
```

```text
ADENOIDECTOMIA E AMIGDALECTOMIA.txt
```

```text
AMIGDALECTOMIA+ADENOIDECTOMIA.txt
```

Exemplo correto:

```text
ADENO - AMIGDALECTOMIA.txt
ADENO - AMIGDALECTOMIA+SEPTOPLASTIA.txt
```

> [!WARNING]
> Atenção: utilize os nomes dos procedimentos exatamente como cadastrados no sistema do hospital.

#### Verifique Adulto e Criança

Caso existam diferenças de prescrição entre adultos e crianças, mantenha arquivos distintos nas respectivas pastas.

### Quando a Receita Não For Encontrada

Se o programa não localizar um modelo correspondente:

1. A receita daquele paciente não será gerada.
2. Uma mensagem será exibida no log do programa.
3. Crie o arquivo correspondente e execute o processamento novamente.

## Primeira Utilização

Na primeira execução, o programa criará automaticamente um arquivo de configuração.

Antes de gerar documentos, é necessário cadastrar os cirurgiões utilizados pelo serviço.

## Cadastro de Cirurgiões

1. Abra o programa.
2. Clique em **Cirurgiões**.
3. Clique em **Adicionar**.
4. Preencha os campos:

   * Nome completo
   * Prefixo `[Dr., Dra., Prof. Dr., Profa. Dra.]`
   * CRM
   * RQE
   * Especialidade
5. Clique em **Salvar**.

Repita o processo para todos os médicos do serviço.

## Editar um Cirurgião

1. Clique em **Cirurgiões**.
1. Selecione o médico desejado.
1. Clique em **Editar**.
1. Atualize as informações necessárias.
1. Clique em **Salvar**.

## Excluir um Cirurgião

1. Clique em **Cirurgiões**.
1. Selecione o médico desejado.
1. Clique em **Excluir**.
1. Confirme a operação.

> Atenção: a exclusão é permanente.

## Problemas Comuns

### O programa não consegue salvar um documento

Verifique se o arquivo está aberto no Microsoft Word.

Feche o documento e tente novamente.

### O cirurgião não está cadastrado

Abra o menu **Cirurgiões** e cadastre o médico informado.

### Nenhum documento foi gerado

Verifique se:

* O PDF correto foi selecionado.
* Os cirurgiões presentes na agenda estão cadastrados.
* Os modelos de receita estão configurados corretamente.

### O programa foi aberto pela primeira vez e não há médicos cadastrados

Clique em **Cirurgiões** e adicione os médicos do serviço antes de gerar documentos.
