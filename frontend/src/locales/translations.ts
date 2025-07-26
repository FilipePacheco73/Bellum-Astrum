const translations = {
  'pt-BR': {
    home: {
      title: 'Bellum Astrum',
      welcome: 'Bem-vindo ao universo de batalhas espaciais!',
      subtitle: 'Explore galáxias distantes, construa sua frota e domine os céus em batalhas épicas!',
      login_button: 'Entrar'
    },
    register: {
      title: 'Criar Conta',
      name: 'Nome',
      email: 'Email',
      password: 'Senha',
      register_button: 'Cadastrar',
      back_to_home: 'Voltar para o início',
      success_register: 'Cadastro realizado com sucesso!',
      error_register: 'Erro ao cadastrar!',
      connection_error: 'Erro de conexão com o servidor!',
      email_already_registered: 'Email já está em uso!',
      nickname_already_registered: 'Nome de usuário já está em uso!',
      server_error: 'Erro interno do servidor. Tente novamente mais tarde.',
      registering: 'Cadastrando...'
    },
    validation: {
      invalid_email: 'Email inválido',
      password_min_length: 'Senha deve ter pelo menos 6 caracteres'
    },
    dashboard: {
      title: 'Dashboard',
      welcome_message: 'Bem-vindo! Você está logado e pode acessar esta página protegida.',
      welcome_title: 'Bem-vindo de volta, {nickname}!',
      subtitle: 'Prepare-se para explorar as galáxias e dominar o espaço',
      loading: 'Carregando dados...',
      load_error: 'Erro ao carregar dados',
      auth_error: 'Erro de autenticação',
      goto_login: 'Ir para Login',
      try_again: 'Tentar novamente',
      user_data_error: 'Erro ao carregar dados do usuário',
      user_not_found: 'Usuário não encontrado',
      data_not_found: 'Dados não encontrados',
      data_not_loaded: 'Não foi possível carregar os dados do usuário',
      unexpected_error: 'Erro inesperado no Dashboard',
      level: 'Nível',
      credits: 'Créditos',
      victories: 'Vitórias',
      win_rate: 'Taxa de Vitória',
      experience_progress: 'Progresso de Experiência',
      xp_next_level: 'XP para o próximo nível',
      battle_stats: 'Estatísticas de Batalha',
      defeats: 'Derrotas',
      total_battles: 'Total de Batalhas',
      elo_rating: 'ELO Rating',
      damage_dealt: 'Dano Causado',
      ships_destroyed: 'Naves Destruídas',
      account_info: 'Informações da Conta',
      email: 'Email',
      user_id: 'ID do Usuário',
      current_rank: 'Patente Atual',
      ship_info: 'Informações de Naves',
      active_ships: 'Naves Ativas',
      available_slots: 'Slots Disponíveis',
      can_activate_more: 'Pode Ativar Mais',
      yes: 'Sim',
      no: 'Não',
      ships_lost: 'Naves Perdidas',
      quick_actions: 'Ações Rápidas',
      my_ships: 'Minhas Naves',
      market: 'Mercado',
      battle: 'Batalha',
      users: 'Usuários',
      stats: {
        battles: 'Batalhas',
        victories: 'Vitórias',
        credits: 'Créditos',
        current_balance: 'Saldo atual',
        damage_dealt: 'Dano Causado',
        total_damage: 'Total de dano',
        defeats: 'Derrotas',
        battles_lost: 'Batalhas perdidas',
        ships_destroyed: 'Naves Destruídas',
        enemies_defeated: 'Inimigos abatidos',
        damage_taken: 'Dano Recebido',
        total_absorbed: 'Total absorvido',
        active_ships: 'Naves Ativas',
        limit_reached: 'Limite atingido',
        slots_free: '{count} slots livres',
        ships_lost: 'Naves Perdidas',
        ships_destroyed_count: 'Naves destruídas'
      },
      activities: {
        title: 'Atividades Recentes',
        no_activities: 'Nenhuma atividade recente encontrada.',
        start_playing: 'Comece jogando para ver suas atividades aqui!'
      },
      additional_stats: {
        experience: 'Experiência',
        damage_taken: 'Dano Recebido',
        max_ships: 'Máximo de Naves'
      },
      ranks: {
        'Recruit': 'Recruta',
        'Ensign': 'Guarda-Marinha',
        'Lieutenant': 'Tenente',
        'Lieutenant Commander': 'Capitão-Tenente',
        'Commander': 'Capitão de Corveta',
        'Captain': 'Capitão de Fragata',
        'Commodore': 'Capitão de Mar e Guerra',
        'Rear Admiral': 'Contra-Almirante',
        'Vice Admiral': 'Vice-Almirante',
        'Admiral': 'Almirante',
        'Fleet Admiral': 'Almirante de Esquadra'
      }
    },
    sidebar: {
      level: 'Nível',
      logout: 'Sair do jogo',
      logout_description: 'Sair do jogo',
      menu_descriptions: {
        dashboard: 'Base de operações',
        ships: 'Gerenciar frota',
        battle: 'Arena de combate',
        market: 'Comprar e vender',
        users: 'Outros jogadores'
      }
    },
    error_boundary: {
      title: 'Oops! Algo deu errado',
      subtitle: 'Um erro inesperado ocorreu na aplicação.',
      error_details: 'Detalhes do Erro:',
      show_stack_trace: 'Mostrar stack trace',
      reload_page: 'Recarregar Página',
      go_home: 'Ir para Home'
    },
    session_expired: {
      title: 'Sessão Expirada',
      message: 'Sua sessão expirou por motivos de segurança. Por favor, faça login novamente para continuar.',
      cancel: 'Cancelar',
      login: 'Fazer Login'
    },
    private_route: {
      checking_auth: 'Verificando autenticação...',
      redirecting: 'Redirecionando para login...'
    },
    errors: {
      login_error: 'Erro ao fazer login!'
    },
    login: {
      title: 'Entrar',
      email: 'Email',
      password: 'Senha',
      login_button: 'Entrar',
      back_to_home: 'Voltar para o início',
      success_login: 'Login realizado com sucesso!',
      invalid_credentials: 'Credenciais inválidas',
      connection_error: 'Erro de conexão com o servidor!',
      server_error: 'Erro interno do servidor. Tente novamente mais tarde.',
      logging_in: 'Entrando...'
    },
    users: {
      title: 'Usuários',
      subtitle: 'Lista de jogadores do Bellum Astrum.'
    },
    ships: {
      title: 'Naves',
      subtitle: 'Veja todas as naves disponíveis no jogo.'
    },
    market: {
      title: 'Mercado',
      subtitle: 'Compre e venda naves espaciais.'
    },
    battle: {
      title: 'Batalha',
      subtitle: 'Inicie batalhas épicas entre naves!'
    },
    navbar: {
      home: 'Home',
      users: 'Usuários',
      ships: 'Naves',
      market: 'Mercado',
      battle: 'Batalha',
      language: 'Idioma'
    },
    common: {
      logo_alt: 'Bellum Astrum Logo'
    },
    footer: {
      rights: 'Todos os direitos reservados.'
    }
  },
  'en-US': {
    home: {
      title: 'Bellum Astrum',
      welcome: 'Welcome to the universe of space battles!',
      subtitle: 'Explore distant galaxies, build your fleet and dominate the skies in epic battles!',
      login_button: 'Login'
    },
    register: {
      title: 'Create Account',
      name: 'Name',
      email: 'Email',
      password: 'Password',
      register_button: 'Register',
      back_to_home: 'Back to Home',
      success_register: 'Registration successful!',
      error_register: 'Registration error!',
      connection_error: 'Connection error with the server!',
      email_already_registered: 'Email already in use!',
      nickname_already_registered: 'Username already in use!',
      server_error: 'Internal server error. Please try again later.',
      registering: 'Registering...'
    },
    validation: {
      invalid_email: 'Invalid email',
      password_min_length: 'Password must be at least 6 characters'
    },
    dashboard: {
      title: 'Dashboard',
      welcome_message: 'Welcome! You are logged in and can access this protected page.',
      welcome_title: 'Welcome back, {nickname}!',
      subtitle: 'Get ready to explore galaxies and dominate space',
      loading: 'Loading data...',
      load_error: 'Error loading data',
      auth_error: 'Authentication error',
      goto_login: 'Go to Login',
      try_again: 'Try again',
      user_data_error: 'Error loading user data',
      user_not_found: 'User not found',
      data_not_found: 'Data not found',
      data_not_loaded: 'Could not load user data',
      unexpected_error: 'Unexpected error in Dashboard',
      level: 'Level',
      credits: 'Credits',
      victories: 'Victories',
      win_rate: 'Win Rate',
      experience_progress: 'Experience Progress',
      xp_next_level: 'XP to next level',
      battle_stats: 'Battle Statistics',
      defeats: 'Defeats',
      total_battles: 'Total Battles',
      elo_rating: 'ELO Rating',
      damage_dealt: 'Damage Dealt',
      ships_destroyed: 'Ships Destroyed',
      account_info: 'Account Information',
      email: 'Email',
      user_id: 'User ID',
      current_rank: 'Current Rank',
      ship_info: 'Ship Information',
      active_ships: 'Active Ships',
      available_slots: 'Available Slots',
      can_activate_more: 'Can Activate More',
      yes: 'Yes',
      no: 'No',
      ships_lost: 'Ships Lost',
      quick_actions: 'Quick Actions',
      my_ships: 'My Ships',
      market: 'Market',
      battle: 'Battle',
      users: 'Users',
      stats: {
        battles: 'Battles',
        victories: 'Victories',
        credits: 'Credits',
        current_balance: 'Current balance',
        damage_dealt: 'Damage Dealt',
        total_damage: 'Total damage',
        defeats: 'Defeats',
        battles_lost: 'Battles lost',
        ships_destroyed: 'Ships Destroyed',
        enemies_defeated: 'Enemies defeated',
        damage_taken: 'Damage Taken',
        total_absorbed: 'Total absorbed',
        active_ships: 'Active Ships',
        limit_reached: 'Limit reached',
        slots_free: '{count} slots free',
        ships_lost: 'Ships Lost',
        ships_destroyed_count: 'Ships destroyed'
      },
      activities: {
        title: 'Recent Activities',
        no_activities: 'No recent activities found.',
        start_playing: 'Start playing to see your activities here!'
      },
      additional_stats: {
        experience: 'Experience',
        damage_taken: 'Damage Taken',
        max_ships: 'Max Ships'
      },
      ranks: {
        'Recruit': 'Recruit',
        'Ensign': 'Ensign',
        'Lieutenant': 'Lieutenant',
        'Lieutenant Commander': 'Lieutenant Commander',
        'Commander': 'Commander',
        'Captain': 'Captain',
        'Commodore': 'Commodore',
        'Rear Admiral': 'Rear Admiral',
        'Vice Admiral': 'Vice Admiral',
        'Admiral': 'Admiral',
        'Fleet Admiral': 'Fleet Admiral'
      }
    },
    sidebar: {
      level: 'Level',
      logout: 'Logout',
      logout_description: 'Exit game',
      menu_descriptions: {
        dashboard: 'Operations base',
        ships: 'Manage fleet',
        battle: 'Combat arena',
        market: 'Buy and sell',
        users: 'Other players'
      }
    },
    error_boundary: {
      title: 'Oops! Something went wrong',
      subtitle: 'An unexpected error occurred in the application.',
      error_details: 'Error Details:',
      show_stack_trace: 'Show stack trace',
      reload_page: 'Reload Page',
      go_home: 'Go to Home'
    },
    session_expired: {
      title: 'Session Expired',
      message: 'Your session has expired for security reasons. Please log in again to continue.',
      cancel: 'Cancel',
      login: 'Login'
    },
    private_route: {
      checking_auth: 'Checking authentication...',
      redirecting: 'Redirecting to login...'
    },
    errors: {
      login_error: 'Login error!'
    },
    login: {
      title: 'Login',
      email: 'Email',
      password: 'Password',
      login_button: 'Login',
      back_to_home: 'Back to Home',
      success_login: 'Login successful!',
      invalid_credentials: 'Invalid credentials',
      connection_error: 'Connection error with the server!',
      server_error: 'Internal server error. Please try again later.',
      logging_in: 'Logging in...'
    },
    users: {
      title: 'Users',
      subtitle: 'List of Bellum Astrum players.'
    },
    ships: {
      title: 'Ships',
      subtitle: 'See all ships available in the game.'
    },
    market: {
      title: 'Market',
      subtitle: 'Buy and sell spaceships.'
    },
    battle: {
      title: 'Battle',
      subtitle: 'Start epic battles between ships!'
    },
    navbar: {
      home: 'Home',
      users: 'Users',
      ships: 'Ships',
      market: 'Market',
      battle: 'Battle',
      language: 'Language'
    },
    common: {
      logo_alt: 'Bellum Astrum Logo'
    },
    footer: {
      rights: 'All rights reserved.'
    }
  }
};

export default translations;
