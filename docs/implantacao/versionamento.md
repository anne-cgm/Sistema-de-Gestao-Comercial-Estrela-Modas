# Política de Versionamento

## 1. Objetivo

Estabelecer um padrão para identificar e controlar as versões das imagens Docker da aplicação Estrela Modas.

## 2. Padrão utilizado

O projeto utiliza Semantic Versioning (SemVer), seguindo o formato MAJOR.MINOR.PATCH.

- MAJOR: alterações incompatíveis com versões anteriores.
- MINOR: adição de funcionalidades compatíveis.
- PATCH: correções de erros e pequenos ajustes.

## 3. Identificação das imagens

Cada imagem Docker deve possuir uma tag específica de versão.

Exemplos:

- estrela-modas:0.1.0
- estrela-modas:0.2.0
- estrela-modas:0.2.1

## 4. Controle das versões

As tags permitem identificar versões específicas da aplicação, facilitando a manutenção, a reprodução de ambientes e a recuperação de versões anteriores.

## 5. Rollback

Caso uma atualização apresente problemas, deve ser possível selecionar uma imagem de versão anterior e executar novamente a aplicação utilizando essa imagem.

## 6. Considerações finais

O versionamento permite maior controle sobre as publicações e contribui para a estabilidade e manutenção da aplicação.