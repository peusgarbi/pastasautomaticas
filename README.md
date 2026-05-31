# Gerador Automático de Pastas

Sistema para geração automática de receitas de alta, atestados médicos e declarações de acompanhante a partir da agenda cirúrgica em PDF.

- Gera pastas de alta com receita e orientações automáticas para os pacientes cirúrgicos do HIORP;
- Faz a **felicidade** dos residentes.

> By [Peusgarb.](https://github.com/peusgarbi)

## Índice

* [Obtendo a Agenda Cirúrgica](#obtendo-a-agenda-cirúrgica)
* [Primeira Utilização](#primeira-utilização)
* [Cadastro de Cirurgiões](#cadastro-de-cirurgiões)
* [Gerando os Documentos](#gerando-os-documentos)
* [Arquivos Gerados](#arquivos-gerados)
* [Limpar Impressos](#limpar-impressos)
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

> Atenção: o sistema foi desenvolvido para processar o relatório "Relatório Farmácia Novo". Outros relatórios podem não ser reconhecidos corretamente.

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

> Atenção: esta ação não pode ser desfeita.

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
