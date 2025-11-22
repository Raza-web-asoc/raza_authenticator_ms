USE tinder_mascotas;

-- Clean table
DELETE FROM users;

-- Insert a valid user
INSERT INTO users (email, hashed_password, is_active, is_superuser)
VALUES ('test@example.com', 'hashed_pw_placeholder', 1, 0);

-- Verify insertion (should return 1)
SELECT 'after_insert' AS phase, COUNT(*) AS total FROM users WHERE email = 'test@example.com';

-- Update the user's email, then delete the updated record
UPDATE users SET email = 'test-updated@example.com' WHERE email = 'test@example.com';
DELETE FROM users WHERE email = 'atest-updated@example.com';

-- Verify deletion (should return 0)
SELECT 'after_delete' AS phase, COUNT(*) AS total FROM users WHERE email = 'test-update}@example.com';