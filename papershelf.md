---
layout: page
title: Papershelf
---

<style>
.papershelf-intro {
  color: var(--text-muted);
  font-size: .95rem;
  margin-bottom: 2.5rem;
  line-height: 1.75;
}

.paper-section {
  margin-bottom: 3rem;
}

.paper-section-title {
  font-size: .68rem;
  font-weight: 700;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--text-subtle);
  margin: 0 0 1.25rem;
  padding-bottom: .65rem;
  border-bottom: 1px solid var(--border-soft);
}

.paper-list {
  display: -webkit-flex;
  display: flex;
  -webkit-flex-direction: column;
          flex-direction: column;
  gap: .85rem;
}

.paper-card {
  padding: 1.15rem 1.35rem;
  background-color: var(--bg-soft);
  border: 1px solid var(--border-soft);
  border-radius: 8px;
  -webkit-transition: border-color .15s ease, background-color .15s ease;
          transition: border-color .15s ease, background-color .15s ease;
}

.paper-card:hover {
  border-color: var(--accent);
  background-color: var(--bg-dark);
}

.paper-card-header {
  display: -webkit-flex;
  display: flex;
  -webkit-justify-content: space-between;
          justify-content: space-between;
  -webkit-align-items: flex-start;
          align-items: flex-start;
  gap: .85rem;
  margin-bottom: .45rem;
}

.paper-title {
  font-size: .975rem;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -.02em;
  line-height: 1.35;
  margin: 0;
}

.paper-title a {
  color: inherit;
  text-decoration: none;
}

.paper-title a:hover {
  color: var(--accent);
  text-decoration: none;
}

.paper-year {
  -webkit-flex-shrink: 0;
          flex-shrink: 0;
  font-size: .68rem;
  font-weight: 700;
  color: var(--accent);
  background-color: var(--accent-light);
  padding: .2rem .55rem;
  border-radius: 4px;
  letter-spacing: .04em;
  margin-top: .1rem;
}

.paper-meta {
  font-size: .78rem;
  color: var(--text-subtle);
  margin: 0 0 .6rem;
  line-height: 1.5;
}

.paper-meta strong {
  color: var(--text-muted);
  font-weight: 600;
}

.paper-desc {
  font-size: .855rem;
  color: var(--text-muted);
  line-height: 1.7;
  margin: 0 0 .85rem;
}

.paper-footer {
  display: -webkit-flex;
  display: flex;
  -webkit-justify-content: space-between;
          justify-content: space-between;
  -webkit-align-items: center;
          align-items: center;
}

.paper-venue {
  font-size: .68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .09em;
  color: var(--text-subtle);
}

.paper-link {
  font-size: .78rem;
  font-weight: 600;
  color: var(--accent);
  text-decoration: none;
}

.paper-link:hover {
  color: var(--accent-hover);
  text-decoration: none;
}
</style>

<p class="papershelf-intro">
  Research papers that shaped distributed systems and machine learning over the last decade.
  A reading list I return to — systems that survived contact with production and ideas that
  became the foundations everything else is built on.
</p>

<section class="paper-section">
  <h2 class="paper-section-title">Distributed Systems &amp; Databases</h2>
  <div class="paper-list">

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://research.google/pubs/spanner-googles-globally-distributed-database/" target="_blank" rel="noopener noreferrer">Spanner: Google's Globally-Distributed Database</a></h3>
        <span class="paper-year">2012</span>
      </div>
      <p class="paper-meta"><strong>Corbett et al.</strong> &mdash; Google Research</p>
      <p class="paper-desc">The first system to distribute data at global scale while supporting externally-consistent distributed transactions. Spanner uses TrueTime—GPS and atomic clocks—to assign commit timestamps that reflect real-world causality. It redefined what production-grade globally-consistent databases could look like and influenced every geo-distributed database built since.</p>
      <div class="paper-footer">
        <span class="paper-venue">OSDI &rsquo;12</span>
        <a href="https://research.google/pubs/spanner-googles-globally-distributed-database/" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://research.facebook.com/publications/tao-facebooks-distributed-data-store-for-the-social-graph/" target="_blank" rel="noopener noreferrer">TAO: Facebook's Distributed Data Store for the Social Graph</a></h3>
        <span class="paper-year">2013</span>
      </div>
      <p class="paper-meta"><strong>Bronson et al.</strong> &mdash; Facebook</p>
      <p class="paper-desc">Facebook's custom graph store serving billions of reads per second with eventual consistency. TAO trades strict consistency for availability, using a tiered cache architecture optimized for the specific access patterns of social graph traversals. A masterclass in pragmatic distributed systems design—building for the actual workload, not the theoretical ideal.</p>
      <div class="paper-footer">
        <span class="paper-venue">USENIX ATC &rsquo;13</span>
        <a href="https://research.facebook.com/publications/tao-facebooks-distributed-data-store-for-the-social-graph/" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://raft.github.io/raft.pdf" target="_blank" rel="noopener noreferrer">In Search of an Understandable Consensus Algorithm (Raft)</a></h3>
        <span class="paper-year">2014</span>
      </div>
      <p class="paper-meta"><strong>Ongaro &amp; Ousterhout</strong> &mdash; Stanford University</p>
      <p class="paper-desc">Introduced Raft as a more understandable alternative to Paxos for achieving consensus in distributed systems. Decomposes the problem into leader election, log replication, and safety—each independently reasoned about. Now the backbone of etcd, CockroachDB, TiKV, and virtually every distributed system built in the last decade that needs fault-tolerant coordination.</p>
      <div class="paper-footer">
        <span class="paper-venue">USENIX ATC &rsquo;14</span>
        <a href="https://raft.github.io/raft.pdf" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/" target="_blank" rel="noopener noreferrer">The Dataflow Model</a></h3>
        <span class="paper-year">2015</span>
      </div>
      <p class="paper-meta"><strong>Akidau et al.</strong> &mdash; Google</p>
      <p class="paper-desc">A unified model for batch and streaming data processing that answers the "what, where, when, and how" of data computation. Built on the experience of Google's internal Millwheel and Flume systems, it gave engineers a principled framework for reasoning about event-time vs. processing-time. The foundation for Apache Beam and the model that ended the "Lambda architecture" era.</p>
      <div class="paper-footer">
        <span class="paper-venue">VLDB &rsquo;15</span>
        <a href="https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://dl.acm.org/doi/10.1145/2882903.2903741" target="_blank" rel="noopener noreferrer">The Snowflake Elastic Data Warehouse</a></h3>
        <span class="paper-year">2016</span>
      </div>
      <p class="paper-meta"><strong>Dageville et al.</strong> &mdash; Snowflake Computing</p>
      <p class="paper-desc">Designed a cloud-native data warehouse that completely decouples storage from compute, enabling each to scale independently. The virtual warehouse model allows multiple concurrent workloads to share storage without I/O contention. Pioneered the multi-cluster shared data architecture that is now the standard across the cloud data warehouse industry.</p>
      <div class="paper-footer">
        <span class="paper-venue">SIGMOD &rsquo;16</span>
        <a href="https://dl.acm.org/doi/10.1145/2882903.2903741" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://dl.acm.org/doi/10.1145/3035918.3056101" target="_blank" rel="noopener noreferrer">Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases</a></h3>
        <span class="paper-year">2017</span>
      </div>
      <p class="paper-meta"><strong>Verbitski et al.</strong> &mdash; Amazon Web Services</p>
      <p class="paper-desc">Reimagined MySQL for cloud environments by replacing the storage layer with a distributed, fault-tolerant log-based system. The core insight: only redo log records need to flow to storage, eliminating the write amplification of traditional databases and reducing network I/O by 7.7x compared to MySQL on EC2. A blueprint for cloud-native database design.</p>
      <div class="paper-footer">
        <span class="paper-venue">SIGMOD &rsquo;17</span>
        <a href="https://dl.acm.org/doi/10.1145/3035918.3056101" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/" target="_blank" rel="noopener noreferrer">Zanzibar: Google's Consistent, Global Authorization System</a></h3>
        <span class="paper-year">2019</span>
      </div>
      <p class="paper-meta"><strong>Patel et al.</strong> &mdash; Google</p>
      <p class="paper-desc">The authorization system enforcing permissions across all of Google's products—Drive, YouTube, Maps, and more. Handles trillions of ACL checks per day with consistent snapshots while maintaining sub-10ms latency at the tail. The relationship-based access control (ReBAC) model it introduced spawned an entire category of open-source projects including OpenFGA and SpiceDB.</p>
      <div class="paper-footer">
        <span class="paper-venue">USENIX ATC &rsquo;19</span>
        <a href="https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://dl.acm.org/doi/10.1145/3318464.3386134" target="_blank" rel="noopener noreferrer">CockroachDB: The Resilient Geo-Distributed SQL Database</a></h3>
        <span class="paper-year">2020</span>
      </div>
      <p class="paper-meta"><strong>Taft et al.</strong> &mdash; Cockroach Labs</p>
      <p class="paper-desc">A distributed SQL database that brings Spanner-style globally-consistent transactions to open-source. Built on RocksDB and Raft for the storage layer, with a full PostgreSQL-compatible SQL engine layered on top. Demonstrated that serializable isolation at geo-distributed scale was practical outside of hyperscalers—a significant proof of concept for the industry.</p>
      <div class="paper-footer">
        <span class="paper-venue">SIGMOD &rsquo;20</span>
        <a href="https://dl.acm.org/doi/10.1145/3318464.3386134" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://dl.acm.org/doi/10.1145/3448016.3457559" target="_blank" rel="noopener noreferrer">FoundationDB: A Distributed Unbundled Transactional Key-Value Store</a></h3>
        <span class="paper-year">2021</span>
      </div>
      <p class="paper-meta"><strong>Zhou et al.</strong> &mdash; Apple / FoundationDB</p>
      <p class="paper-desc">An ACID key-value store that deliberately unbundles transaction processing from storage, enabling independent scaling of each. The simulation-based testing framework—capable of reproducing and replaying any sequence of events including disk failures and network partitions—has become legendary in the distributed systems community as a gold standard for correctness testing.</p>
      <div class="paper-footer">
        <span class="paper-venue">SIGMOD &rsquo;21</span>
        <a href="https://dl.acm.org/doi/10.1145/3448016.3457559" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://www.usenix.org/conference/atc22/presentation/elhemali" target="_blank" rel="noopener noreferrer">Amazon DynamoDB: A Scalable, Predictably Performant, and Fully Managed NoSQL Database Service</a></h3>
        <span class="paper-year">2022</span>
      </div>
      <p class="paper-meta"><strong>Elhemali et al.</strong> &mdash; Amazon Web Services</p>
      <p class="paper-desc">A retrospective on 10+ years of operating DynamoDB at scale, revealing architectural evolutions not documented elsewhere. Details the shift to per-request cost-based admission control, the introduction of global tables, and the hard-won lessons around providing predictable single-digit millisecond latency at any scale. Essential reading for anyone building or operating a database service.</p>
      <div class="paper-footer">
        <span class="paper-venue">USENIX ATC &rsquo;22</span>
        <a href="https://www.usenix.org/conference/atc22/presentation/elhemali" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

  </div>
</section>

<section class="paper-section">
  <h2 class="paper-section-title">Machine Learning &amp; AI</h2>
  <div class="paper-list">

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/1301.3781" target="_blank" rel="noopener noreferrer">Efficient Estimation of Word Representations in Vector Space (Word2Vec)</a></h3>
        <span class="paper-year">2013</span>
      </div>
      <p class="paper-meta"><strong>Mikolov et al.</strong> &mdash; Google</p>
      <p class="paper-desc">Introduced two architectures—CBOW and Skip-gram—for learning high-quality word vector representations from large text corpora with surprising efficiency. The resulting vectors capture semantic and syntactic relationships, famously demonstrating that "king − man + woman ≈ queen". Laid the groundwork for all subsequent representation learning research in NLP.</p>
      <div class="paper-footer">
        <span class="paper-venue">arXiv 2013</span>
        <a href="https://arxiv.org/abs/1301.3781" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/1406.2661" target="_blank" rel="noopener noreferrer">Generative Adversarial Nets</a></h3>
        <span class="paper-year">2014</span>
      </div>
      <p class="paper-meta"><strong>Goodfellow et al.</strong> &mdash; Université de Montréal</p>
      <p class="paper-desc">Proposed training two networks simultaneously—a generator creating synthetic data and a discriminator distinguishing real from fake—via a minimax adversarial game. This framework proved remarkably generative, spawning photorealistic image synthesis, data augmentation, and ultimately the entire modern generative AI wave. One of the most-cited ML papers of all time.</p>
      <div class="paper-footer">
        <span class="paper-venue">NeurIPS &rsquo;14</span>
        <a href="https://arxiv.org/abs/1406.2661" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/1512.03385" target="_blank" rel="noopener noreferrer">Deep Residual Learning for Image Recognition (ResNet)</a></h3>
        <span class="paper-year">2015</span>
      </div>
      <p class="paper-meta"><strong>He et al.</strong> &mdash; Microsoft Research</p>
      <p class="paper-desc">Introduced residual connections (skip connections) that allow gradients to flow directly through networks, enabling training of 100+ layer deep networks without degradation. Won ILSVRC 2015 with a top-5 error rate of 3.57%—surpassing human performance. The residual connection became one of the most universally adopted building blocks in deep learning across every domain.</p>
      <div class="paper-footer">
        <span class="paper-venue">CVPR &rsquo;16</span>
        <a href="https://arxiv.org/abs/1512.03385" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/1706.03762" target="_blank" rel="noopener noreferrer">Attention Is All You Need</a></h3>
        <span class="paper-year">2017</span>
      </div>
      <p class="paper-meta"><strong>Vaswani et al.</strong> &mdash; Google Brain</p>
      <p class="paper-desc">Proposed the Transformer architecture, replacing recurrent and convolutional layers entirely with multi-head self-attention. Enabled massively parallel training and dramatically better handling of long-range dependencies compared to RNNs. Arguably the single most impactful ML paper of the past decade—it underpins GPT, BERT, and every modern large language model.</p>
      <div class="paper-footer">
        <span class="paper-venue">NeurIPS &rsquo;17</span>
        <a href="https://arxiv.org/abs/1706.03762" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/1810.04805" target="_blank" rel="noopener noreferrer">BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding</a></h3>
        <span class="paper-year">2018</span>
      </div>
      <p class="paper-meta"><strong>Devlin et al.</strong> &mdash; Google AI Language</p>
      <p class="paper-desc">Demonstrated that deep bidirectional pre-training on masked language modeling followed by task-specific fine-tuning achieves state-of-the-art results across 11 NLP benchmarks simultaneously. The key insight: models benefit enormously from seeing context from both directions at once. Changed how the entire NLP community approaches new tasks—fine-tune, don't train from scratch.</p>
      <div class="paper-footer">
        <span class="paper-venue">NAACL &rsquo;19</span>
        <a href="https://arxiv.org/abs/1810.04805" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/2005.14165" target="_blank" rel="noopener noreferrer">Language Models are Few-Shot Learners (GPT-3)</a></h3>
        <span class="paper-year">2020</span>
      </div>
      <p class="paper-meta"><strong>Brown et al.</strong> &mdash; OpenAI</p>
      <p class="paper-desc">Showed that scaling language models to 175B parameters produces emergent few-shot learning abilities—performing novel tasks from just a handful of examples in the prompt, without any gradient updates. Introduced the concept of in-context learning that underpins prompt engineering today. The paper that made the broader world take LLMs seriously as general-purpose tools.</p>
      <div class="paper-footer">
        <span class="paper-venue">NeurIPS &rsquo;20</span>
        <a href="https://arxiv.org/abs/2005.14165" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/2006.11239" target="_blank" rel="noopener noreferrer">Denoising Diffusion Probabilistic Models</a></h3>
        <span class="paper-year">2020</span>
      </div>
      <p class="paper-meta"><strong>Ho, Jain &amp; Abbeel</strong> &mdash; UC Berkeley</p>
      <p class="paper-desc">Established the theoretical and practical foundation for modern diffusion-based generative models. By framing image generation as iterative denoising of Gaussian noise, DDPM achieved quality competitive with GANs while being significantly more stable and principled to train. The direct ancestor of Stable Diffusion, DALL-E 2, Imagen, and every modern text-to-image system.</p>
      <div class="paper-footer">
        <span class="paper-venue">NeurIPS &rsquo;20</span>
        <a href="https://arxiv.org/abs/2006.11239" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://www.nature.com/articles/s41586-021-03819-2" target="_blank" rel="noopener noreferrer">Highly Accurate Protein Structure Prediction with AlphaFold</a></h3>
        <span class="paper-year">2021</span>
      </div>
      <p class="paper-meta"><strong>Jumper et al.</strong> &mdash; Google DeepMind</p>
      <p class="paper-desc">Solved the 50-year-old grand challenge of computational biology: predicting a protein's 3D structure from its amino acid sequence, with near-experimental accuracy. AlphaFold2's Evoformer architecture combines multiple sequence alignments with structural reasoning through specialized attention layers. Released a database of 200M+ predicted structures, accelerating drug discovery and biology research globally.</p>
      <div class="paper-footer">
        <span class="paper-venue">Nature &rsquo;21</span>
        <a href="https://www.nature.com/articles/s41586-021-03819-2" target="_blank" rel="noopener noreferrer" class="paper-link">Read paper ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/2103.00020" target="_blank" rel="noopener noreferrer">Learning Transferable Visual Models From Natural Language Supervision (CLIP)</a></h3>
        <span class="paper-year">2021</span>
      </div>
      <p class="paper-meta"><strong>Radford et al.</strong> &mdash; OpenAI</p>
      <p class="paper-desc">Trained a vision encoder and text encoder jointly via contrastive learning on 400M internet image-text pairs, producing models that generalize to new visual concepts zero-shot by comparing image embeddings to text descriptions. CLIP demonstrated that natural language is a richer supervision signal than fixed label sets. Became a foundation component for multimodal AI and semantic image search.</p>
      <div class="paper-footer">
        <span class="paper-venue">ICML &rsquo;21</span>
        <a href="https://arxiv.org/abs/2103.00020" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/2203.02155" target="_blank" rel="noopener noreferrer">Training Language Models to Follow Instructions with Human Feedback (InstructGPT)</a></h3>
        <span class="paper-year">2022</span>
      </div>
      <p class="paper-meta"><strong>Ouyang et al.</strong> &mdash; OpenAI</p>
      <p class="paper-desc">Introduced the RLHF (Reinforcement Learning from Human Feedback) pipeline to align language model outputs with human intent. By fine-tuning GPT-3 on human-rated comparisons, InstructGPT produced models that were simultaneously more helpful, honest, and less harmful than the base model despite being 100x smaller. The alignment technique that powers ChatGPT and every instruction-tuned LLM since.</p>
      <div class="paper-footer">
        <span class="paper-venue">NeurIPS &rsquo;22</span>
        <a href="https://arxiv.org/abs/2203.02155" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/2303.08774" target="_blank" rel="noopener noreferrer">GPT-4 Technical Report</a></h3>
        <span class="paper-year">2023</span>
      </div>
      <p class="paper-meta"><strong>OpenAI</strong></p>
      <p class="paper-desc">Documents GPT-4, OpenAI's first multimodal model accepting both text and image inputs. Achieves human-level performance on professional benchmarks including the bar exam (90th percentile) and medical licensing exams. The report also details a novel risk assessment and red-teaming methodology for large models—setting a new standard for responsible pre-deployment evaluation that the industry began to follow.</p>
      <div class="paper-footer">
        <span class="paper-venue">arXiv 2023</span>
        <a href="https://arxiv.org/abs/2303.08774" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/2302.13971" target="_blank" rel="noopener noreferrer">LLaMA: Open and Efficient Foundation Language Models</a></h3>
        <span class="paper-year">2023</span>
      </div>
      <p class="paper-meta"><strong>Touvron et al.</strong> &mdash; Meta AI</p>
      <p class="paper-desc">Released a series of open-source language models (7B–65B parameters) trained exclusively on publicly available data, showing that smaller carefully-trained models could match GPT-3. Democratized LLM research by giving the community a capable open base to build on. Spawned an ecosystem of fine-tunes—Alpaca, Vicuna, Mistral, and hundreds more—that collectively reshaped the open-source AI landscape.</p>
      <div class="paper-footer">
        <span class="paper-venue">arXiv 2023</span>
        <a href="https://arxiv.org/abs/2302.13971" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/2312.00752" target="_blank" rel="noopener noreferrer">Mamba: Linear-Time Sequence Modeling with Selective State Spaces</a></h3>
        <span class="paper-year">2023</span>
      </div>
      <p class="paper-meta"><strong>Gu &amp; Dao</strong> &mdash; Carnegie Mellon / Princeton</p>
      <p class="paper-desc">Proposed a sequence model based on state space models (SSMs) with an input-dependent selection mechanism—matching or exceeding Transformer performance on language modeling while scaling linearly with sequence length instead of quadratically. Challenged the assumption that attention is necessary for high-quality sequence modeling and reignited interest in SSMs as a viable alternative architecture.</p>
      <div class="paper-footer">
        <span class="paper-venue">arXiv 2023</span>
        <a href="https://arxiv.org/abs/2312.00752" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

    <div class="paper-card">
      <div class="paper-card-header">
        <h3 class="paper-title"><a href="https://arxiv.org/abs/2312.11805" target="_blank" rel="noopener noreferrer">Gemini: A Family of Highly Capable Multimodal Models</a></h3>
        <span class="paper-year">2023</span>
      </div>
      <p class="paper-meta"><strong>Gemini Team</strong> &mdash; Google DeepMind</p>
      <p class="paper-desc">Google DeepMind's natively multimodal model family trained jointly on text, images, audio, video, and code from the ground up—rather than retrofitting vision onto a language model. Gemini Ultra was the first model to surpass human expert performance on MMLU. Demonstrated that native multimodality at training time produces substantially better cross-modal reasoning than post-hoc fusion approaches.</p>
      <div class="paper-footer">
        <span class="paper-venue">arXiv 2023</span>
        <a href="https://arxiv.org/abs/2312.11805" target="_blank" rel="noopener noreferrer" class="paper-link">arXiv ↗</a>
      </div>
    </div>

  </div>
</section>
