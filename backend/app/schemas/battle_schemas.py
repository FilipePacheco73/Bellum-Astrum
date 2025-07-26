from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


class BattleRequest(BaseModel):
    """
    Request model for battles with formation strategies.
    
    Attributes:
        opponent_user_id (int): ID of the opponent user
        user_ship_numbers (Union[int, List[int]]): Ship number(s) for current user
        opponent_ship_numbers (Union[int, List[int]]): Ship number(s) for opponent
        user_formation (Optional[str]): Formation strategy for current user ("DEFENSIVE", "AGGRESSIVE", "TACTICAL")
                                       If None, uses user's default_formation
        opponent_formation (Optional[str]): Formation strategy for opponent ("DEFENSIVE", "AGGRESSIVE", "TACTICAL")
                                           If None, uses opponent's default_formation
    """
    opponent_user_id: int
    user_ship_numbers: Union[int, List[int]]
    opponent_ship_numbers: Union[int, List[int]]
    user_formation: Optional[str] = None
    opponent_formation: Optional[str] = None


class BattleParticipant(BaseModel):
    """
    Representa um participante de uma batalha.
    
    Atributos:
        user_id (int): ID do usuário participante.
        nickname (str): Apelido do usuário.
        ship_number (int): Número único da nave usada na batalha.
        ship_name (str): Nome da nave.
        attack (float): Poder de ataque da nave.
        shield (float): Força do escudo da nave.
        evasion (float): Capacidade de evasão da nave.
        fire_rate (float): Taxa de disparo da nave.
        hp (float): Pontos de vida da nave.
        value (int): Valor monetário ou estratégico da nave.
    """
    user_id: int
    nickname: str
    ship_number: int
    ship_name: str
    attack: float
    shield: float
    evasion: float
    fire_rate: float
    hp: float
    value: int

class BattleHistoryResponse(BaseModel):
    """
    Modelo de resposta para o histórico de uma batalha.
    
    Atributos:
        battle_id (int): ID único da batalha.
        timestamp (datetime): Data e hora da batalha.
        participants (List[BattleParticipant]): Lista de participantes com suas naves.
        winner_user_id (Optional[int]): ID do usuário vencedor (ou None para empate).
        battle_log (List[str]): Log detalhado dos eventos da batalha.
        extra (Optional[Dict[str, Any]]): Informações adicionais (formações, danos, etc.).
    """
    battle_id: int
    timestamp: datetime
    participants: List[BattleParticipant]
    winner_user_id: Optional[int] = None
    battle_log: List[str]
    extra: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)
