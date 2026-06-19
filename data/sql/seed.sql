INSERT INTO projects VALUES
('P-1001', 'Riverside Office Renovation', 'Sacramento, CA', 'Riverside Holdings', 'Northstar Builders');

INSERT INTO project_schedule VALUES
('A205', 'P-1001', 'Concrete Pour - Foundation', '2026-03-13', '2026-03-13', '2026-03-17', '2026-03-17', 'Complete', 3, 'Weather'),
('A310', 'P-1001', 'Electrical Rough-In', '2026-03-18', '2026-03-22', '2026-03-20', '2026-03-25', 'Complete', 2, 'Design Clarification'),
('A420', 'P-1001', 'Flooring Installation', '2026-04-05', '2026-04-10', NULL, NULL, 'Planned', 0, NULL);

INSERT INTO site_notes (project_id, note_date, author, category, note_text) VALUES
('P-1001', '2026-03-12', 'Site Superintendent', 'Weather', 'Heavy rain started at 9:00 AM. Concrete work preparation slowed.'),
('P-1001', '2026-03-13', 'Site Superintendent', 'Site Condition', 'Standing water observed near foundation area. Concrete pour postponed.'),
('P-1001', '2026-03-14', 'Safety Manager', 'Safety', 'Concrete pour marked unsafe due to wet site conditions.'),
('P-1001', '2026-03-15', 'Project Manager', 'Notice', 'Potential delay notice prepared for owner review.');

INSERT INTO rfi_logs VALUES
('RFI-014', 'P-1001', '2026-03-16', 'Structural detail conflicts with architectural plan near east wall.', 'Use revised structural detail issued March 18.', 'Electrical rough-in delayed by 2 days.', 'Closed');

INSERT INTO weather_records (project_id, weather_date, location, precipitation_inches, max_wind_mph, condition_summary) VALUES
('P-1001', '2026-03-12', 'Sacramento, CA', 1.25, 22, 'Heavy rain'),
('P-1001', '2026-03-13', 'Sacramento, CA', 1.80, 28, 'Heavy rain'),
('P-1001', '2026-03-14', 'Sacramento, CA', 0.95, 18, 'Rain and wet site');

INSERT INTO change_orders VALUES
('CO-001', 'P-1001', 'Weather Delay - Site Preparation', 'Weather delay', '2026-02-19', 2, 0.00, 'Approved', 2, 0.00, 'Approved due to abnormal rainfall and timely notice.'),
('CO-002', 'P-1001', 'Owner Requested Flooring Upgrade', 'Scope change', '2026-03-02', 0, 18500.00, 'Approved', 0, 17250.00, 'Approved as owner-directed scope upgrade.'),
('CO-003', 'P-1001', 'Crew Shortage Delay', 'Labor shortage', '2026-03-05', 2, 0.00, 'Rejected', 0, 0.00, 'Rejected because contractor labor shortage is not excusable under contract.');
