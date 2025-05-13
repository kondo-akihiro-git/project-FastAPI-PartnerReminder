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
