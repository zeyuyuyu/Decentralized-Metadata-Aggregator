import abc
from typing import Dict, Any, List
import importlib
import pkgutil
import logging

class MetadataParser(abc.ABC):
    """Abstract base class for metadata parsers"""
    
    @abc.abstractmethod
    def can_handle(self, data: bytes) -> bool:
        """Check if this parser can handle the given data"""
        pass
        
    @abc.abstractmethod
    def extract_metadata(self, data: bytes) -> Dict[str, Any]:
        """Extract metadata from the given data"""
        pass

class ParserRegistry:
    """Registry and loader for metadata parser plugins"""
    
    def __init__(self):
        self._parsers: List[MetadataParser] = []
        self.logger = logging.getLogger(__name__)
        
    def register_parser(self, parser: MetadataParser) -> None:
        """Register a new metadata parser"""
        if not isinstance(parser, MetadataParser):
            raise TypeError(f"Parser must inherit from MetadataParser, got {type(parser)}")
        self._parsers.append(parser)
        self.logger.info(f"Registered parser: {parser.__class__.__name__}")
        
    def load_parsers(self, package_name: str = 'parsers') -> None:
        """Dynamically load all parser plugins from a package"""
        try:
            package = importlib.import_module(package_name)
            for _, name, _ in pkgutil.iter_modules(package.__path__):
                try:
                    module = importlib.import_module(f'{package_name}.{name}')
                    for item in dir(module):
                        obj = getattr(module, item)
                        if isinstance(obj, type) and issubclass(obj, MetadataParser) \\
                           and obj != MetadataParser:
                            self.register_parser(obj())
                except Exception as e:
                    self.logger.error(f"Failed to load parser {name}: {str(e)}")
        except ImportError as e:
            self.logger.error(f"Failed to import parser package: {str(e)}")
            
    def parse(self, data: bytes) -> Dict[str, Any]:
        """Parse metadata using the first compatible parser"""
        for parser in self._parsers:
            try:
                if parser.can_handle(data):
                    return parser.extract_metadata(data)
            except Exception as e:
                self.logger.error(f"Parser {parser.__class__.__name__} failed: {str(e)}")
                continue
        
        raise ValueError("No compatible parser found for the given data")

# Example usage:
'''
registry = ParserRegistry()
registry.load_parsers()

# Process some data
try:
    metadata = registry.parse(some_binary_data)
except ValueError as e:
    print(f"Failed to parse metadata: {str(e)}")
'''