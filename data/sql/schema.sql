CREATE TABLE projects (
    project_id VARCHAR(20) PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    location VARCHAR(150),
    owner_name VARCHAR(150),
    contractor_name VARCHAR(150)
);

CREATE TABLE project_schedule (
    activity_id VARCHAR(20) PRIMARY KEY,
    project_id VARCHAR(20),
    activity_name VARCHAR(150),
    planned_start DATE,
    planned_finish DATE,
    actual_start DATE,
    actual_finish DATE,
    status VARCHAR(50),
    delay_days INT,
    responsible_party VARCHAR(100)
);

CREATE TABLE site_notes (
    note_id SERIAL PRIMARY KEY,
    project_id VARCHAR(20),
    note_date DATE,
    author VARCHAR(100),
    category VARCHAR(50),
    note_text TEXT
);

CREATE TABLE rfi_logs (
    rfi_id VARCHAR(20) PRIMARY KEY,
    project_id VARCHAR(20),
    submitted_date DATE,
    question TEXT,
    response TEXT,
    impact_summary TEXT,
    status VARCHAR(50)
);

CREATE TABLE weather_records (
    record_id SERIAL PRIMARY KEY,
    project_id VARCHAR(20),
    weather_date DATE,
    location VARCHAR(150),
    precipitation_inches DECIMAL(5,2),
    max_wind_mph INT,
    condition_summary VARCHAR(150)
);

CREATE TABLE change_orders (
    co_id VARCHAR(20) PRIMARY KEY,
    project_id VARCHAR(20),
    title VARCHAR(150),
    reason VARCHAR(100),
    submitted_date DATE,
    requested_days INT,
    requested_cost DECIMAL(12,2),
    status VARCHAR(50),
    approved_days INT,
    approved_cost DECIMAL(12,2),
    summary TEXT
);
