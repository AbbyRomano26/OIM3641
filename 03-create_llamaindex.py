import os
from pathlib import Path
from dotenv import load_dotenv
from llama_cloud_services import LlamaCloudIndex, LlamaParse

load_dotenv()

API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not set")

data_path = Path("data/Internet History Sourcebooks_ Modern History.pdf")

parser = LlamaParse(api_key=API_KEY)

if data_path.exists():
    job_result = parser.parse(str(data_path))
else:
    raise FileNotFoundError(f'file not found: {data_path}')

documents = job_result.get_text_documents()
if not documents:
    raise RuntimeError('No documents returned')

print(f"Parse OK. First 120 chars:\n{documents[0].text[:120]}\n")

index_name = 'abby_test_index'
index = LlamaCloudIndex.from_documents(documents, name=index_name)

print(f"Created index: {index_name}")
print(f'Index ID: {index.id}')
