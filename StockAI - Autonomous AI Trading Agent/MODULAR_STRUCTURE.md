# 🏗️ StockAI Modular Structure Documentation

## 📊 Overview

The StockAI project has been reorganized from a monolithic structure into a proper modular architecture with clear separation of concerns, better maintainability, and Docker containerization support.

## 🎯 Key Improvements

### **1. Modular Package Structure**
- **Clear separation** of concerns into logical modules
- **Proper Python packages** with `__init__.py` files
- **Import organization** for better code maintainability
- **Scalable architecture** for future enhancements

### **2. Configuration Management**
- **Environment-based configuration** using Pydantic
- **Type-safe settings** with validation
- **Easy deployment** across different environments
- **Secure credential management**

### **3. Docker Containerization**
- **Multi-container setup** with docker-compose
- **Database integration** (PostgreSQL + Redis)
- **Monitoring stack** (Prometheus + Grafana)
- **Easy deployment** and scaling

### **4. Development Tools**
- **Makefile** for common development tasks
- **Code formatting** and linting tools
- **Testing framework** with pytest
- **Logging utilities** for better debugging

## 📁 Directory Structure

```
StockAI - Autonomous AI Trading Agent/
├── src/                            # Source code
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # Application entry point
│   ├── core/                       # Core business logic
│   │   ├── __init__.py
│   │   ├── decision_engine.py      # Decision making
│   │   └── portfolio_manager.py    # Portfolio management
│   ├── agents/                     # Analytical agents
│   │   ├── __init__.py
│   │   ├── data_fetcher.py         # Data acquisition
│   │   ├── execution_agent.py      # Trade execution
│   │   ├── fundamentals_agent.py   # Financial analysis
│   │   ├── technicals_agent.py     # Technical analysis
│   │   ├── valuation_agent.py      # Valuation analysis
│   │   ├── sentiment_agent.py      # Sentiment analysis
│   │   └── risk_manager.py         # Risk assessment
│   ├── models/                     # ML models
│   │   ├── __init__.py
│   │   ├── ensemble_model.py       # RL ensemble
│   │   └── training_modedl.py      # Model training
│   ├── data/                       # Data processing
│   │   ├── __init__.py
│   │   └── preprocessor.py         # Feature engineering
│   ├── utils/                      # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py               # Logging
│   │   └── validators.py           # Validation
│   └── config/                     # Configuration
│       ├── __init__.py
│       └── settings.py             # Settings management
├── tests/                          # Test suite
│   ├── unit/                       # Unit tests
│   └── integration/                # Integration tests
├── docker/                         # Docker configs
│   ├── init.sql                    # DB initialization
│   └── grafana/                    # Monitoring dashboards
├── logs/                           # Application logs
├── models/                         # Trained models
├── data/                           # Data storage
├── Dockerfile                      # Container definition
├── docker-compose.yml              # Multi-container setup
├── Makefile                        # Development commands
├── requirements.txt                # Dependencies
├── env.example                     # Environment template
└── README.md                       # Documentation
```

## 🔧 Key Components

### **Core Module (`src/core/`)**
- **DecisionEngine**: Orchestrates the 4 Agents + 5 RL Models workflow
- **PortfolioManager**: Manages portfolio state and decisions

### **Agents Module (`src/agents/`)**
- **DataFetcher**: Real-time market data acquisition
- **FundamentalsAgent**: Company financial analysis
- **TechnicalsAgent**: Technical analysis and indicators
- **ValuationAgent**: Intrinsic value calculations
- **SentimentAgent**: Market sentiment analysis
- **RiskManager**: Risk assessment and management
- **ExecutionAgent**: Trade execution via Alpaca API

### **Models Module (`src/models/`)**
- **EnsembleRLModel**: 5-model RL ensemble (SAC, PPO, A2C, DQN, TD3)
- **Training**: Model training and evaluation

### **Data Module (`src/data/`)**
- **DataPreprocessor**: Feature engineering for RL models
- **Technical Indicators**: 14 required indicators calculation

### **Utils Module (`src/utils/`)**
- **Logger**: Structured logging with file and console output
- **Validators**: Input validation and sanitization

### **Config Module (`src/config/`)**
- **Settings**: Environment-based configuration management
- **Type Safety**: Pydantic models for configuration validation

## 🐳 Docker Architecture

### **Services:**
1. **stockai**: Main application container
2. **postgres**: PostgreSQL database
3. **redis**: Redis cache and message queue
4. **prometheus**: Metrics collection
5. **grafana**: Monitoring dashboards

### **Benefits:**
- **Isolated environments** for development and production
- **Easy scaling** with container orchestration
- **Consistent deployment** across different platforms
- **Built-in monitoring** and logging

## 🚀 Development Workflow

### **Setup:**
```bash
make setup          # Initial project setup
make install        # Install dependencies
```

### **Development:**
```bash
make dev           # Run locally
make test          # Run tests
make format        # Format code
make lint          # Run linting
```

### **Docker:**
```bash
make run           # Start with Docker
make logs          # View logs
make stop          # Stop containers
make clean         # Clean up
```

### **Monitoring:**
```bash
make monitor       # Open monitoring dashboards
```

## 📊 Configuration Management

### **Environment Variables:**
- **ALPACA_API_KEY**: Alpaca API key
- **ALPACA_API_SECRET**: Alpaca API secret
- **STOCK_LIST**: Comma-separated stock symbols
- **CONFIDENCE_THRESHOLD**: Minimum confidence for trades
- **DATABASE_URL**: Database connection string
- **REDIS_HOST**: Redis server host

### **Settings Class:**
```python
from src.config.settings import get_settings

settings = get_settings()
print(settings.stock_list)  # ['AAPL', 'TSLA', 'GOOGL']
```

## 🧪 Testing

### **Unit Tests:**
- **Validators**: Input validation testing
- **Models**: ML model testing
- **Utils**: Utility function testing

### **Integration Tests:**
- **End-to-end workflows**
- **API integration testing**
- **Database operations**

### **Running Tests:**
```bash
make test                    # Run all tests
pytest tests/unit/          # Run unit tests only
pytest tests/integration/   # Run integration tests only
```

## 📈 Monitoring & Logging

### **Logging:**
- **Structured logging** with timestamps
- **File and console output**
- **Configurable log levels**
- **Module-specific loggers**

### **Monitoring:**
- **Prometheus metrics** collection
- **Grafana dashboards** for visualization
- **Health checks** for all services
- **Performance monitoring**

## 🔒 Security Features

### **Input Validation:**
- **Stock symbol validation**
- **Trade signal validation**
- **Quantity and confidence validation**
- **Input sanitization**

### **Configuration Security:**
- **Environment variable management**
- **Secure credential storage**
- **Type-safe configuration**
- **Validation of all inputs**

## 🚀 Deployment

### **Local Development:**
```bash
make setup
make dev
```

### **Docker Deployment:**
```bash
make run
```

### **Production Deployment:**
- **Kubernetes manifests** (future)
- **CI/CD pipeline** (future)
- **Auto-scaling** (future)

## 📚 Benefits of Modular Structure

### **1. Maintainability**
- **Clear separation** of concerns
- **Easy to locate** and modify code
- **Reduced coupling** between components
- **Better code organization**

### **2. Scalability**
- **Independent scaling** of components
- **Easy addition** of new features
- **Microservices-ready** architecture
- **Container-based deployment**

### **3. Testing**
- **Isolated unit tests** for each module
- **Integration testing** capabilities
- **Mock-friendly** architecture
- **Comprehensive test coverage**

### **4. Development Experience**
- **Clear project structure**
- **Easy onboarding** for new developers
- **Consistent coding patterns**
- **Automated development tools**

This modular structure provides a solid foundation for the StockAI trading system, making it more maintainable, scalable, and production-ready! 🚀
