# Error messages for all the site
error_sold_out_product = 'O estoque deste produto acabou'
error_quantity_exceeded = 'A quantidade máxima deste produto foi excedida. Você não poderá adicionar mais ao seu carrinho'
error_cart_empty = 'O seu carrinho está vazio no momento!'
error_login_required = 'Você precisa estar logado para fazer isto'
error_form_not_valid = 'Algum campo de seu formulário está incorreto. Verifique e tente novamente'
error_cpf_used = 'Este CPF já está sendo utilizado'
error_cpf_not_valid = 'Este CPF não é valido. Veja se o digitou corretamente e tente novamente'
error_cep_not_valid = 'O seu CEP não é valido. Digite apenas os números e tente novamente'


# Success messages for all the site
success_register_done = 'Seu registro foi feito com sucesso! Agora logue e aproveite nosso site'
success_logout = 'Você foi deslogado com sucesso'
success_order_created = 'Seu pedido foi criado com sucessp'


def success_login(user):
    return f'Seja bem vindo ao nosso site, {user.first_name}!'
