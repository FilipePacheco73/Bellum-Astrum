export const battleTranslations = {
  'pt-BR': {
    battle: {
      title: 'Arena de Batalha',
      subtitle: 'Escolha seu modo de batalha e desafie oponentes',
      modes: {
        npc: 'Batalha vs NPC',
        pvp: 'Batalha PvP'
      },
      sections: {
        choose_npc: 'Escolha seu Oponente NPC',
        choose_opponent: 'Escolha seu Oponente'
      },
      labels: {
        level: 'Nível',
        rank: 'Rank',
        elo: 'ELO',
        victories: 'Vitórias',
        defeats: 'Derrotas',
        fleet: 'Frota',
        ships: 'naves'
      },
      actions: {
        battle: 'Batalhar',
        challenge: 'Desafiar',
        battling: 'Batalhando...'
      },
      messages: {
        loading: 'Carregando dados de batalha...',
        no_players: 'Nenhum jogador disponível para batalha no momento.',
        no_npcs: 'Nenhum NPC disponível para batalha no momento.',
        no_ships_available: 'Você não possui naves ativas para batalha',
        opponent_no_ships: 'O oponente não possui naves ativas para batalha!',
        load_error: 'Não foi possível carregar dados de batalha. Tente novamente.',
        no_active_ships: 'Nenhuma nave ativa',
        npc_no_ships: 'Este NPC não possui naves ativas para batalha'
      },
      notifications: {
        victory_title: '🎉 VITÓRIA!',
        victory_message: 'Você venceu a batalha #{battleId}! Parabéns, comandante!',
        defeat_title: '💥 DERROTA!',
        defeat_message: 'Você foi derrotado na batalha #{battleId}. Melhore suas naves e tente novamente!',
        draw_title: '🤝 EMPATE!',
        draw_message: 'A batalha #{battleId} terminou em empate. Foi uma luta equilibrada!',
        error_title: 'Falha na Batalha',
        error_message: 'Não foi possível iniciar a batalha: {error}',
        unknown_error: 'Erro desconhecido',
        no_ships_title: 'Nenhuma Nave Ativa',
        no_ships_message: 'Você precisa de pelo menos uma nave ativa para batalhar! Vá em "Minhas Naves" para ativar uma nave.',
        view_log: 'Ver Log'
      },
      fleet_modal: {
        title: 'Frota',
        summary: 'Resumo da Frota',
        no_ships: 'Nenhuma nave na frota',
        total_ships: 'Total de Naves',
        total_attack: 'Ataque Total',
        total_shield: 'Escudo Total',
        total_hp: 'HP Total',
        view_fleet: 'Ver Frota'
      }
    },
    battle_log: {
      title: 'Log da Batalha',
      close: 'Fechar',
      participants: 'Participantes da Batalha',
      battle_statistics: 'Estatísticas da Batalha',
      round: 'Rodada',
      victory: 'VITÓRIA!',
      defeat: 'DERROTA!',
      draw: 'EMPATE!',
      result_messages: {
        victory: 'Parabéns! Você venceu a batalha!',
        defeat: 'Você foi derrotado nesta batalha.',
        draw: 'A batalha terminou em empate.'
      },
      stats: {
        attack: 'Ataque',
        shield: 'Escudo',
        hp: 'HP',
        fire_rate: 'Taxa de Tiro',
        evasion: 'Evasão',
        value: 'Valor',
        base: 'Base',
        current: 'Atual'
      },
      ship: 'Nave',
      winner: 'Vencedor'
    }
  },
  'en-US': {
    battle: {
      title: 'Battle Arena',
      subtitle: 'Choose your battle mode and challenge opponents',
      modes: {
        npc: 'Battle vs NPC',
        pvp: 'PvP Battle'
      },
      sections: {
        choose_npc: 'Choose your NPC Opponent',
        choose_opponent: 'Choose your Opponent'
      },
      labels: {
        level: 'Level',
        rank: 'Rank',
        elo: 'ELO',
        victories: 'Victories',
        defeats: 'Defeats',
        fleet: 'Fleet',
        ships: 'ships'
      },
      actions: {
        battle: 'Battle',
        challenge: 'Challenge',
        battling: 'Battling...'
      },
      messages: {
        loading: 'Loading battle data...',
        no_players: 'No players available for battle at the moment.',
        no_npcs: 'No NPCs available for battle at the moment.',
        no_ships_available: 'You don\'t have active ships for battle',
        opponent_no_ships: 'Opponent doesn\'t have active ships for battle!',
        load_error: 'Could not load battle data. Please try again.',
        no_active_ships: 'No active ships',
        npc_no_ships: 'This NPC has no active ships for battle'
      },
      notifications: {
        victory_title: '🎉 VICTORY!',
        victory_message: 'You won battle #{battleId}! Congratulations, commander!',
        defeat_title: '💥 DEFEAT!',
        defeat_message: 'You were defeated in battle #{battleId}. Improve your ships and try again!',
        draw_title: '🤝 DRAW!',
        draw_message: 'Battle #{battleId} ended in a draw. It was a balanced fight!',
        error_title: 'Battle Failed',
        error_message: 'Could not start battle: {error}',
        unknown_error: 'Unknown error',
        no_ships_title: 'No Active Ships',
        no_ships_message: 'You need at least one active ship to battle! Go to "My Ships" to activate a ship.',
        view_log: 'View Log'
      },
      fleet_modal: {
        title: 'Fleet',
        summary: 'Fleet Summary',
        no_ships: 'No ships in fleet',
        total_ships: 'Total Ships',
        total_attack: 'Total Attack',
        total_shield: 'Total Shield',
        total_hp: 'Total HP',
        view_fleet: 'View Fleet'
      }
    },
    battle_log: {
      title: 'Battle Log',
      close: 'Close',
      participants: 'Battle Participants',
      battle_statistics: 'Battle Statistics',
      round: 'Round',
      victory: 'VICTORY!',
      defeat: 'DEFEAT!',
      draw: 'DRAW!',
      result_messages: {
        victory: 'Congratulations! You won the battle!',
        defeat: 'You were defeated in this battle.',
        draw: 'The battle ended in a draw.'
      },
      stats: {
        attack: 'Attack',
        shield: 'Shield',
        hp: 'HP',
        fire_rate: 'Fire Rate',
        evasion: 'Evasion',
        value: 'Value',
        base: 'Base',
        current: 'Current'
      },
      ship: 'Ship',
      winner: 'Winner'
    }
  }
};
