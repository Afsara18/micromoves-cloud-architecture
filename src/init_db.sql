-- Micromoves Relational Database Initialization Matrix
-- Target Environment: Amazon RDS PostgreSQL Node Cluster

CREATE TABLE IF NOT EXISTS operational_moving_logs (
    log_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    distance_miles NUMERIC(6, 2) NOT NULL,
    crew_size INT NOT NULL,
    demand_multiplier NUMERIC(3, 1) NOT NULL,
    calculated_quote_total NUMERIC(8, 2) NOT NULL,
    transaction_integrity_status VARCHAR(20) DEFAULT 'SUCCESS'
);

-- Seed verification baseline matching active interface metrics
INSERT INTO operational_moving_logs (distance_miles, crew_size, demand_multiplier, calculated_quote_total)
VALUES (50.00, 3, 1.2, 408.00);
