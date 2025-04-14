-- Insert test speed test records if there are no records
DO $$
BEGIN
    -- Check if speed_test_records table is empty
    IF NOT EXISTS (SELECT 1 FROM speed_test_records LIMIT 1) THEN
        -- Insert seed data only if the table is empty
        INSERT INTO speed_test_records (timestamp, download_speed, upload_speed, latency, time_of_day, server_name, server_url)
        VALUES
          ('2025-03-01 08:00:00+00', 120.5, 15.3, 12.5, 'MORNING', 'Test Server 1', 'https://server1.test'),
          ('2025-03-01 14:00:00+00', 115.2, 14.9, 13.1, 'AFTERNOON', 'Test Server 1', 'https://server1.test'),
          ('2025-03-01 20:00:00+00', 130.9, 6.8, 4.2, 'EVENING', 'Test Server 1', 'https://server1.test'),
          ('2025-03-02 08:00:00+00', 120.5, 15.3, 12.5, 'MORNING', 'Test Server 1', 'https://server1.test'),
          ('2025-03-02 14:00:00+00', 115.2, 14.9, 13.1, 'AFTERNOON', 'Test Server 1', 'https://server1.test'),
          ('2025-03-02 20:00:00+00', 130.9, 6.8, 4.2, 'EVENING', 'Test Server 1', 'https://server1.test'),
          ('2025-03-03 08:00:00+00', 120.5, 15.3, 12.5, 'MORNING', 'Test Server 1', 'https://server1.test'),
          ('2025-03-03 14:00:00+00', 115.2, 14.9, 13.1, 'AFTERNOON', 'Test Server 1', 'https://server1.test'),
          ('2025-03-03 20:00:00+00', 130.9, 6.8, 4.2, 'EVENING', 'Test Server 1', 'https://server1.test'),
          ('2025-03-04 08:00:00+00', 120.5, 15.3, 12.5, 'MORNING', 'Test Server 1', 'https://server1.test'),
          ('2025-03-04 14:00:00+00', 115.2, 14.9, 13.1, 'AFTERNOON', 'Test Server 1', 'https://server1.test'),
          ('2025-03-04 20:00:00+00', 130.9, 6.8, 4.2, 'EVENING', 'Test Server 1', 'https://server1.test');

        RAISE NOTICE 'Inserted test data: 12 speed test records';
    ELSE
        RAISE NOTICE 'Speed test records already exist, skipping test data generation';
    END IF;
END $$;