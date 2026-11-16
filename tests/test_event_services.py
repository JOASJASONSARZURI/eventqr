import csv
import io
from datetime import date, datetime

from app.models.entities import Attendance, Event, Participant
from app.models.user import User
from app.services.checkin_service import CheckInResult, CheckInService
from app.services.export_service import ExportService


def create_participant(session, name="Ana Pérez", email="ana@example.com"):
    user = User(username="propietario", hashed_password="hash")
    session.add(user)
    session.commit()
    session.refresh(user)

    event = Event(
        name="Conferencia",
        date=date(2026, 5, 1),
        user_id=user.id,
    )
    session.add(event)
    session.commit()
    session.refresh(event)

    participant = Participant(
        event_id=event.id,
        name=name,
        email=email,
        token="token-de-prueba",
    )
    session.add(participant)
    session.commit()
    session.refresh(participant)
    return event, participant


def test_check_in_allows_only_one_attendance_per_day(session):
    _, participant = create_participant(session)
    service = CheckInService(session)
    today = date(2026, 5, 1)

    assert service.check_in(participant.token, date=today) == CheckInResult.OK
    assert (
        service.check_in(participant.token, date=today)
        == CheckInResult.YA_REGISTRADO_HOY
    )
    assert service.check_in(participant.token, date=date(2026, 5, 2)) == CheckInResult.OK
    assert service.check_in("token-invalido", date=today) == CheckInResult.TOKEN_INVALIDO


def test_check_in_integrity_error_is_reported_as_duplicate(session, monkeypatch):
    _, participant = create_participant(session)
    attendance_date = date(2026, 5, 1)
    session.add(
        Attendance(
            participant_id=participant.id,
            date=attendance_date,
        )
    )
    session.commit()

    service = CheckInService(session)
    original_lookup = service.attendance_repo.get_by_participant_and_date
    lookup_count = 0

    def miss_first_lookup(participant_id, check_date):
        nonlocal lookup_count
        lookup_count += 1
        if lookup_count == 1:
            return None
        return original_lookup(participant_id, check_date)

    monkeypatch.setattr(
        service.attendance_repo,
        "get_by_participant_and_date",
        miss_first_lookup,
    )

    assert (
        service.check_in(participant.token, date=attendance_date)
        == CheckInResult.YA_REGISTRADO_HOY
    )


def test_export_attendance_csv_uses_utf8_bom_and_date_range(session):
    event, participant = create_participant(session)
    session.add_all(
        [
            Attendance(
                participant_id=participant.id,
                date=date(2026, 5, 1),
                created_at=datetime(2026, 5, 1, 9, 15, 30),
            ),
            Attendance(
                participant_id=participant.id,
                date=date(2026, 5, 3),
                created_at=datetime(2026, 5, 3, 10, 0, 0),
            ),
        ]
    )
    session.commit()

    content = ExportService(session).export_attendance_csv(
        event.id,
        date(2026, 5, 1),
        date(2026, 5, 2),
    )

    assert content.startswith(b"\xef\xbb\xbf")
    rows = list(csv.reader(io.StringIO(content.decode("utf-8-sig"))))
    assert rows == [
        ["Participante", "Correo", "Fecha", "Hora"],
        ["Ana Pérez", "ana@example.com", "2026-05-01", "09:15:30"],
    ]
