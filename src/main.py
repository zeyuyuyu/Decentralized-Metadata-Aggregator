import os
import asyncio
from typing import List
from .agents import MetadataCrawlerAgent, IndexingAgent
from .governance import GovernanceProtocol

async def main():
    """Main entry point for the Decentralized Metadata Aggregator."""
    # Initialize the decentralized governance protocol
    governance_protocol = GovernanceProtocol()

    # Spawn the metadata crawler agents
    crawler_agents: List[MetadataCrawlerAgent] = []
    for _ in range(10):
        crawler_agents.append(MetadataCrawlerAgent(governance_protocol))

    # Spawn the indexing agents
    indexing_agents: List[IndexingAgent] = []
    for _ in range(5):
        indexing_agents.append(IndexingAgent(governance_protocol))

    # Start the agents and the governance protocol
    await asyncio.gather(
        *[agent.start() for agent in crawler_agents],
        *[agent.start() for agent in indexing_agents],
        governance_protocol.start()
    )

if __name__ == "__main__":
    main()