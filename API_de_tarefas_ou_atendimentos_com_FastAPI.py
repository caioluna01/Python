from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Gerenciador de Tarefas",
    description="API para gerenciar tarefas com operações CRUD",
    version="1.0.0",
)

# Schemas


class TarefaBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=100, description="Título da tarefa")
    descricao: Optional[str] = Field(None, max_length=500, description="Descrição opcional")
    concluida: bool = Field(False, description="Status de conclusão")


class TarefaCreate(TarefaBase):
    """Payload para criar uma tarefa (sem ID, sem timestamps)."""
    pass


class TarefaUpdate(BaseModel):
    """Todos os campos opcionais para atualização parcial (PATCH)."""
    titulo: Optional[str] = Field(None, min_length=1, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    concluida: Optional[bool] = None


class TarefaResponse(TarefaBase):
    """Representação completa retornada pela API."""
    id: int
    criada_em: datetime
    atualizada_em: datetime

    class Config:
        from_attributes = True


# "Banco de dados" em memória

class _DB:
    """Encapsula o estado em memória e elimina variáveis globais."""

    def __init__(self):
        self._tarefas: dict[int, TarefaResponse] = {}
        self._next_id: int = 1

    # --- helpers internos ---

    def _get_or_404(self, tarefa_id: int) -> TarefaResponse:
        tarefa = self._tarefas.get(tarefa_id)
        if tarefa is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarefa {tarefa_id} não encontrada",
            )
        return tarefa

    # --- operações CRUD ---

    def criar(self, dados: TarefaCreate) -> TarefaResponse:
        agora = datetime.now()
        tarefa = TarefaResponse(
            id=self._next_id,
            criada_em=agora,
            atualizada_em=agora,
            **dados.model_dump(),
        )
        self._tarefas[self._next_id] = tarefa
        self._next_id += 1
        return tarefa

    def listar(self) -> list[TarefaResponse]:
        return list(self._tarefas.values())

    def buscar(self, tarefa_id: int) -> TarefaResponse:
        return self._get_or_404(tarefa_id)

    def atualizar(self, tarefa_id: int, dados: TarefaUpdate) -> TarefaResponse:
        tarefa = self._get_or_404(tarefa_id)

        campos = dados.model_dump(exclude_unset=True)
        tarefa_dict = tarefa.model_dump()
        tarefa_dict.update(campos)
        tarefa_dict["atualizada_em"] = datetime.now()

        tarefa_atualizada = TarefaResponse(**tarefa_dict)
        self._tarefas[tarefa_id] = tarefa_atualizada
        return tarefa_atualizada

    def deletar(self, tarefa_id: int) -> None:
        self._get_or_404(tarefa_id)
        del self._tarefas[tarefa_id]


db = _DB()

# Rotas

@app.post(
    "/tarefas",
    response_model=TarefaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova tarefa",
)
def criar_tarefa(tarefa: TarefaCreate):
    return db.criar(tarefa)


@app.get(
    "/tarefas",
    response_model=list[TarefaResponse],
    summary="Listar todas as tarefas",
)
def listar_tarefas():
    return db.listar()


@app.get(
    "/tarefas/{tarefa_id}",
    response_model=TarefaResponse,
    summary="Buscar tarefa por ID",
)
def buscar_tarefa(tarefa_id: int):
    return db.buscar(tarefa_id)


@app.patch(
    "/tarefas/{tarefa_id}",
    response_model=TarefaResponse,
    summary="Atualizar tarefa parcialmente",
)
def atualizar_tarefa(tarefa_id: int, dados: TarefaUpdate):
    return db.atualizar(tarefa_id, dados)


@app.delete(
    "/tarefas/{tarefa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar tarefa",
)
def deletar_tarefa(tarefa_id: int):
    db.deletar(tarefa_id)
