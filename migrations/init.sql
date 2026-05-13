"""Database migration initialization script"""

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create batteries table
CREATE TABLE IF NOT EXISTS batteries (
    id SERIAL PRIMARY KEY,
    battery_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id),
    battery_type VARCHAR(100) NOT NULL,
    nominal_voltage FLOAT NOT NULL,
    nominal_capacity FLOAT NOT NULL,
    max_charge_current FLOAT NOT NULL,
    max_discharge_current FLOAT NOT NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create raw_cycles table
CREATE TABLE IF NOT EXISTS raw_cycles (
    id SERIAL PRIMARY KEY,
    battery_id INTEGER NOT NULL REFERENCES batteries(id),
    timestamp TIMESTAMP NOT NULL,
    voltage FLOAT NOT NULL,
    current FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    capacity FLOAT,
    internal_resistance FLOAT,
    re FLOAT,
    rct FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create engineered_features table
CREATE TABLE IF NOT EXISTS engineered_features (
    id SERIAL PRIMARY KEY,
    battery_id INTEGER NOT NULL REFERENCES batteries(id),
    timestamp TIMESTAMP NOT NULL,
    dv_dt FLOAT,
    di_dt FLOAT,
    dt_dt FLOAT,
    power FLOAT,
    energy FLOAT,
    capacity_fraction FLOAT,
    resistance_growth FLOAT,
    features_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create soc_predictions table
CREATE TABLE IF NOT EXISTS soc_predictions (
    id SERIAL PRIMARY KEY,
    battery_id INTEGER NOT NULL REFERENCES batteries(id),
    timestamp TIMESTAMP NOT NULL,
    soc FLOAT NOT NULL,
    confidence FLOAT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create soh_predictions table
CREATE TABLE IF NOT EXISTS soh_predictions (
    id SERIAL PRIMARY KEY,
    battery_id INTEGER NOT NULL REFERENCES batteries(id),
    timestamp TIMESTAMP NOT NULL,
    soh FLOAT NOT NULL,
    degradation_rate FLOAT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create digital_twin_states table
CREATE TABLE IF NOT EXISTS digital_twin_states (
    id SERIAL PRIMARY KEY,
    battery_id INTEGER NOT NULL REFERENCES batteries(id),
    timestamp TIMESTAMP NOT NULL,
    soc FLOAT NOT NULL,
    soh FLOAT NOT NULL,
    internal_resistance FLOAT,
    state_vector JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create forecasts table
CREATE TABLE IF NOT EXISTS forecasts (
    id SERIAL PRIMARY KEY,
    battery_id INTEGER NOT NULL REFERENCES batteries(id),
    forecast_horizon_hours INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    future_soc JSON,
    future_soh JSON,
    future_resistance JSON,
    confidence FLOAT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create anomaly_logs table
CREATE TABLE IF NOT EXISTS anomaly_logs (
    id SERIAL PRIMARY KEY,
    battery_id INTEGER NOT NULL REFERENCES batteries(id),
    timestamp TIMESTAMP NOT NULL,
    severity VARCHAR(50) NOT NULL,
    anomaly_type VARCHAR(100) NOT NULL,
    description TEXT,
    confidence FLOAT,
    metadata JSON,
    is_acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create maintenance_actions table
CREATE TABLE IF NOT EXISTS maintenance_actions (
    id SERIAL PRIMARY KEY,
    battery_id INTEGER NOT NULL REFERENCES batteries(id),
    timestamp TIMESTAMP NOT NULL,
    recommendation VARCHAR(500) NOT NULL,
    priority VARCHAR(50) NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_batteries_user_id ON batteries(user_id);
CREATE INDEX idx_raw_cycles_battery_id ON raw_cycles(battery_id);
CREATE INDEX idx_raw_cycles_timestamp ON raw_cycles(timestamp);
CREATE INDEX idx_soc_predictions_battery_id ON soc_predictions(battery_id);
CREATE INDEX idx_soc_predictions_timestamp ON soc_predictions(timestamp);
CREATE INDEX idx_soh_predictions_battery_id ON soh_predictions(battery_id);
CREATE INDEX idx_soh_predictions_timestamp ON soh_predictions(timestamp);
CREATE INDEX idx_digital_twin_battery_id ON digital_twin_states(battery_id);
CREATE INDEX idx_digital_twin_timestamp ON digital_twin_states(timestamp);
CREATE INDEX idx_forecasts_battery_id ON forecasts(battery_id);
CREATE INDEX idx_anomaly_battery_id ON anomaly_logs(battery_id);
CREATE INDEX idx_anomaly_timestamp ON anomaly_logs(timestamp);
CREATE INDEX idx_maintenance_battery_id ON maintenance_actions(battery_id);
