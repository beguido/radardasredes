-- Adiciona campos de engajamento e foto
ALTER TABLE instagram_profiles ADD COLUMN profile_picture_url TEXT;
ALTER TABLE instagram_profiles ADD COLUMN avg_engagement_rate REAL DEFAULT 0;
ALTER TABLE instagram_profiles ADD COLUMN total_likes INTEGER DEFAULT 0;
ALTER TABLE instagram_profiles ADD COLUMN total_comments INTEGER DEFAULT 0;
ALTER TABLE instagram_profiles ADD COLUMN posts_analyzed INTEGER DEFAULT 0;
