import time
from utils.knowledge_base import Create_Moorad_Embedding, Create_FTP_Embedding, Create_Reports_Embedding
from utils.ai import client
from utils.embedding import Moorad_Embedding, FTP_Embedding, Reports_Embedding
from langchain_huggingface import HuggingFaceEmbeddings

class Moorad_QueryHandler:
    def __init__(self, embeddings_model, knowledge_base, client, rules):
        self.corrections = []
        self.embeddings_model = embeddings_model
        self.knowledge_base = knowledge_base
        self.client = client
        self.conversation_history = []
        self.rules = rules

    def handle_query(self, question):
        self.embeddings_model = HuggingFaceEmbeddings()
        self.client = client
        self.knowledge_base = Moorad_Embedding.knowledge_base
        start_time = time.time()
        calculate_similarity = Create_Moorad_Embedding.calculate_similarity
        
        question_embedding = self.embeddings_model.embed_query(question)

        best_match = None
        highest_similarity = 0
        for correction in self.corrections:
            corrected_question_embedding = self.embeddings_model.embed_query(correction["question"])
            similarity = calculate_similarity(question_embedding, corrected_question_embedding)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = correction

        if best_match and highest_similarity > 0.8:
            corrected_answer = best_match["correct_answer"]
            return f"Answer: {corrected_answer} (Corrected Answer)", []

        retriever = self.knowledge_base.as_retriever()
        retrieved_docs = retriever.invoke(question)

        doc_metadata = {}
        images = []
        for doc in retrieved_docs:
            page = doc.metadata.get("page", "Unknown")
            doc_images = doc.metadata.get("images", [])
            source_info = f"Page {page}"

            if source_info not in doc_metadata:
                doc_metadata[source_info] = {"pages": [], "images": []}
            if page not in doc_metadata[source_info]["pages"]:
                doc_metadata[source_info]["pages"].append(page)
            doc_metadata[source_info]["images"].extend(doc_images)

            images.extend(doc_images)

            combined_text = "\n".join([doc.page_content for doc in retrieved_docs])

            self.conversation_history.append({"role": "user", "content": question})

            messages = [
                {"role": "system", "content": f"{self.rules} Context: {combined_text}"}
            ]
            messages.extend(self.conversation_history)

            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3-8b-chat-hf",
                messages=messages,
                temperature=0.8,
                max_tokens=2048,
            )

            formatted_metadata = []
        for source, data in doc_metadata.items():
            pages_str = ", ".join([str(p) for p in data["pages"]])
            formatted_metadata.append(f"{source}: Pages {pages_str}")
            if data["images"]:
                image_files = ", ".join(data["images"])
                formatted_metadata.append(f"Images: {image_files}")

            metadata_str = "; ".join(formatted_metadata)
            answer_with_context = f"Answer: {response.choices[0].message.content} ({metadata_str})"

            return answer_with_context, images
        
class FTP_QueryHandler:
    def __init__(self, embeddings_model, knowledge_base, client, rules):
        self.corrections = []
        self.embeddings_model = embeddings_model
        self.knowledge_base = knowledge_base
        self.client = client
        self.conversation_history = []
        self.rules = rules

    def handle_query(self, question):
        self.embeddings_model = HuggingFaceEmbeddings()
        self.client = client
        self.knowledge_base = FTP_Embedding.knowledge_base
        start_time = time.time()
        calculate_similarity = Create_FTP_Embedding.calculate_similarity
        
        question_embedding = self.embeddings_model.embed_query(question)

        best_match = None
        highest_similarity = 0
        for correction in self.corrections:
            corrected_question_embedding = self.embeddings_model.embed_query(correction["question"])
            similarity = calculate_similarity(question_embedding, corrected_question_embedding)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = correction

        if best_match and highest_similarity > 0.8:
            corrected_answer = best_match["correct_answer"]
            return f"Answer: {corrected_answer} (Corrected Answer)", []

        retriever = self.knowledge_base.as_retriever()
        retrieved_docs = retriever.invoke(question)

        doc_metadata = {}
        images = []
        for doc in retrieved_docs:
            page = doc.metadata.get("page", "Unknown")
            doc_images = doc.metadata.get("images", [])
            source_info = f"Page {page}"

            if source_info not in doc_metadata:
                doc_metadata[source_info] = {"pages": [], "images": []}
            if page not in doc_metadata[source_info]["pages"]:
                doc_metadata[source_info]["pages"].append(page)
            doc_metadata[source_info]["images"].extend(doc_images)

            images.extend(doc_images)

            combined_text = "\n".join([doc.page_content for doc in retrieved_docs])

            self.conversation_history.append({"role": "user", "content": question})

            messages = [
                {"role": "system", "content": f"{self.rules} Context: {combined_text}"}
            ]
            messages.extend(self.conversation_history)

            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3-8b-chat-hf",
                messages=messages,
                temperature=0.8,
                max_tokens=2048,
            )

            formatted_metadata = []
        for source, data in doc_metadata.items():
            pages_str = ", ".join([str(p) for p in data["pages"]])
            formatted_metadata.append(f"{source}: Pages {pages_str}")
            if data["images"]:
                image_files = ", ".join(data["images"])
                formatted_metadata.append(f"Images: {image_files}")

            metadata_str = "; ".join(formatted_metadata)
            answer_with_context = f"Answer: {response.choices[0].message.content} ({metadata_str})"

            return answer_with_context, images
        
class Reports_QueryHandler:
    def __init__(self, embeddings_model, knowledge_base, client, rules):
        self.corrections = []
        self.embeddings_model = embeddings_model
        self.knowledge_base = knowledge_base
        self.client = client
        self.conversation_history = []
        self.rules = rules

    def handle_query(self, question):
        self.embeddings_model = HuggingFaceEmbeddings()
        self.client = client
        self.knowledge_base = Reports_Embedding.knowledge_base
        start_time = time.time()
        calculate_similarity = Create_Reports_Embedding.calculate_report_similarity
        
        question_embedding = self.embeddings_model.embed_query(question)

        best_match = None
        highest_similarity = 0
        for correction in self.corrections:
            corrected_question_embedding = self.embeddings_model.embed_query(correction["question"])
            similarity = calculate_similarity(question_embedding, corrected_question_embedding)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = correction

        if best_match and highest_similarity > 0.8:
            corrected_answer = best_match["correct_answer"]
            return f"Answer: {corrected_answer} (Corrected Answer)", []

        retriever = self.knowledge_base.as_retriever()
        retrieved_docs = retriever.invoke(question)

        doc_metadata = {}
        images = []
        for doc in retrieved_docs:
            page = doc.metadata.get("page", "Unknown")
            doc_images = doc.metadata.get("images", [])
            source_info = f"Page {page}"

            if source_info not in doc_metadata:
                doc_metadata[source_info] = {"pages": [], "images": []}
            if page not in doc_metadata[source_info]["pages"]:
                doc_metadata[source_info]["pages"].append(page)
            doc_metadata[source_info]["images"].extend(doc_images)

            images.extend(doc_images)

            combined_text = "\n".join([doc.page_content for doc in retrieved_docs])

            self.conversation_history.append({"role": "user", "content": question})

            messages = [
                {"role": "system", "content": f"{self.rules} Context: {combined_text}"}
            ]
            messages.extend(self.conversation_history)

            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3-8b-chat-hf",
                messages=messages,
                temperature=0.8,
                max_tokens=2048,
            )

            formatted_metadata = []
        for source, data in doc_metadata.items():
            pages_str = ", ".join([str(p) for p in data["pages"]])
            formatted_metadata.append(f"{source}: Pages {pages_str}")
            if data["images"]:
                image_files = ", ".join(data["images"])
                formatted_metadata.append(f"Images: {image_files}")

            metadata_str = "; ".join(formatted_metadata)
            answer_with_context = f"Answer: {response.choices[0].message.content} ({metadata_str})"

            return answer_with_context, images