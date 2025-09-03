-- Create the database
CREATE DATABASE IF NOT EXISTS educhain;
USE educhain;

-- Table: Users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,  -- Use hashed passwords in production
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Courses
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    tags TEXT,  -- For ML recommendation (e.g. "python beginner data science")
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: User_Courses (tracks progress and completion)
CREATE TABLE IF NOT EXISTS user_courses (
    user_id INT,
    course_id INT,
    progress INT DEFAULT 0,        -- % of course completed
    completed BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);

-- Table: Certificates
CREATE TABLE IF NOT EXISTS certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    cert_hash VARCHAR(256) NOT NULL,    -- Blockchain hash
    issue_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
);
