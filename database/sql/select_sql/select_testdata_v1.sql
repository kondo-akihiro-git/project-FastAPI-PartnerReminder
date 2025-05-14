SELECT
  m.id AS meeting_id,
  m.title AS title,
  m.date AS date,
  e.event_name AS event,
  pgp.good_point AS partner_good_point
FROM Meetings m
LEFT JOIN EventNames e ON m.id = e.meeting_id
LEFT JOIN PartnerGoodPoints pgp ON m.id = pgp.meeting_id
ORDER BY m.id;


SELECT
  m.id,
  m.title,
  m.location,
  m.date,
  ma.image_path AS my_appearance_image_path,
  en.event_name,
  pa.appearance AS partner_appearance,
  tt.topic AS talked_topic,
  pgp.good_point AS partner_good_point,
  tfn.todo AS todo_for_next
FROM Meetings m
LEFT JOIN MyAppearances ma ON ma.meeting_id = m.id
LEFT JOIN EventNames en ON en.meeting_id = m.id
LEFT JOIN PartnerAppearances pa ON pa.meeting_id = m.id
LEFT JOIN TalkedTopics tt ON tt.meeting_id = m.id
LEFT JOIN PartnerGoodPoints pgp ON pgp.meeting_id = m.id
LEFT JOIN TodoForNext tfn ON tfn.meeting_id = m.id
WHERE m.id = %(meeting_id)s;
