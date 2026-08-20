from app.models.schemas import ResearchQuery, ResearchResponse
from app.retrieval.vector_store import VectorStoreService
from app.rag.chain import RAGChainPipeline
from app.evaluation.evaluator import RAGEvaluator


class ResearchService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.rag_chain = RAGChainPipeline()
        self.evaluator = RAGEvaluator()

    async def process_query(self, request: ResearchQuery) -> ResearchResponse:
        # 1. Retrieve relevant contexts
        sources = await self.vector_store.search(request.query, top_k=request.top_k)

        # 2. Synthesize answer using RAG pipeline
        answer = await self.rag_chain.generate_answer(request.query, sources)

        # 3. Evaluate response quality
        eval_metrics = self.evaluator.evaluate_response(request.query, answer, sources)

        return ResearchResponse(
            query=request.query,
            answer=answer,
            sources=sources,
            evaluation=eval_metrics,
        )
