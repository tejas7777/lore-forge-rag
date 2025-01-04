class Chunker:
   def __init__(self, chunk_size=512, overlap=50):
       self.chunk_size = chunk_size
       self.overlap = overlap

   def chunk_document(self, document):
       content = document['content'].decode()
       chunks = []

       paragraphs = content.split('\n')
       
       current_chunk = ""
       for paragraph in paragraphs:
           if len(current_chunk) + len(paragraph) <= self.chunk_size:
               current_chunk += paragraph + "\n"
           else:
               if current_chunk:
                   chunks.append({
                       "text": current_chunk,
                       "doc_id": document['_id'],
                       "metadata": {
                           "timestamp": document['uploadedAt']
                       }
                   })
               overlap_text = current_chunk[-self.overlap:] if self.overlap > 0 else ""
               current_chunk = overlap_text + paragraph + "\n"
               
       if current_chunk:
           chunks.append({
               "text": current_chunk,
               "doc_id": document['_id'],
               "metadata": {
                   "timestamp": document['uploadedAt']
               }
           })
           
       return chunks