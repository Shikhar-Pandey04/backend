import numpy as np
import hashlib
from typing import List

def generate_mock_embedding(text: str, dimension: int = 384) -> List[float]:
    """
    Generate a mock embedding vector for text
    Uses a deterministic approach based on text hash for consistency
    """
    
    # Create a hash of the text for deterministic results
    text_hash = hashlib.md5(text.encode()).hexdigest()
    
    # Use the hash to seed numpy random generator
    seed = int(text_hash[:8], 16) % (2**32)
    np.random.seed(seed)
    
    # Generate random vector
    embedding = np.random.normal(0, 1, dimension)
    
    # Normalize to unit vector (common for embeddings)
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm
    
    return embedding.tolist()

def generate_semantic_embedding(text: str, dimension: int = 384) -> List[float]:
    """
    Generate a more semantically-aware mock embedding
    Groups similar contract terms together
    """
    
    # Define semantic clusters for contract terms
    semantic_clusters = {
        'termination': ['terminate', 'end', 'cancel', 'expire', 'dissolution'],
        'payment': ['pay', 'invoice', 'billing', 'fee', 'cost', 'price', 'compensation'],
        'liability': ['liable', 'responsibility', 'damages', 'loss', 'harm', 'injury'],
        'confidential': ['confidential', 'secret', 'proprietary', 'private', 'nda'],
        'intellectual_property': ['ip', 'patent', 'copyright', 'trademark', 'invention'],
        'employment': ['employee', 'worker', 'staff', 'hire', 'job', 'position'],
        'license': ['license', 'permit', 'authorization', 'grant', 'right'],
        'renewal': ['renew', 'extend', 'continue', 'auto-renew', 'rollover'],
        'breach': ['breach', 'violation', 'default', 'non-compliance', 'failure'],
        'force_majeure': ['force majeure', 'act of god', 'unforeseeable', 'beyond control']
    }
    
    text_lower = text.lower()
    
    # Find which cluster this text belongs to
    cluster_scores = {}
    for cluster, keywords in semantic_clusters.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            cluster_scores[cluster] = score
    
    # Generate base embedding
    base_embedding = generate_mock_embedding(text, dimension)
    
    # If text matches semantic clusters, adjust embedding
    if cluster_scores:
        # Get the dominant cluster
        dominant_cluster = max(cluster_scores.keys(), key=lambda k: cluster_scores[k])
        
        # Create cluster-specific adjustments
        cluster_adjustments = {
            'termination': [0.8, -0.2, 0.5, 0.3],
            'payment': [0.2, 0.9, -0.1, 0.4],
            'liability': [-0.3, 0.1, 0.8, -0.2],
            'confidential': [0.5, 0.3, -0.4, 0.7],
            'intellectual_property': [0.6, -0.5, 0.2, 0.8],
            'employment': [-0.1, 0.7, 0.4, -0.3],
            'license': [0.4, 0.2, -0.6, 0.5],
            'renewal': [0.3, -0.4, 0.6, 0.2],
            'breach': [-0.8, 0.1, -0.3, 0.4],
            'force_majeure': [0.1, -0.7, 0.3, -0.5]
        }
        
        # Apply cluster adjustment to first few dimensions
        adjustment = cluster_adjustments.get(dominant_cluster, [0, 0, 0, 0])
        for i, adj in enumerate(adjustment):
            if i < len(base_embedding):
                base_embedding[i] = base_embedding[i] * 0.7 + adj * 0.3
    
    return base_embedding

def calculate_similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """
    Calculate cosine similarity between two embeddings
    """
    
    # Convert to numpy arrays
    vec1 = np.array(embedding1)
    vec2 = np.array(embedding2)
    
    # Calculate cosine similarity
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    similarity = dot_product / (norm1 * norm2)
    return float(similarity)

def get_embedding_stats(embeddings: List[List[float]]) -> dict:
    """
    Get statistics about a collection of embeddings
    """
    
    if not embeddings:
        return {}
    
    embeddings_array = np.array(embeddings)
    
    return {
        'count': len(embeddings),
        'dimension': len(embeddings[0]),
        'mean_norm': float(np.mean([np.linalg.norm(emb) for emb in embeddings])),
        'std_norm': float(np.std([np.linalg.norm(emb) for emb in embeddings])),
        'mean_values': embeddings_array.mean(axis=0).tolist(),
        'std_values': embeddings_array.std(axis=0).tolist()
    }
