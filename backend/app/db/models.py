from sqlalchemy import Date, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    project_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    project_name: Mapped[str] = mapped_column(String(150), nullable=False)
    location: Mapped[str | None] = mapped_column(String(150))
    owner_name: Mapped[str | None] = mapped_column(String(150))
    contractor_name: Mapped[str | None] = mapped_column(String(150))


class ProjectSchedule(Base):
    __tablename__ = "project_schedule"

    activity_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    project_id: Mapped[str | None] = mapped_column(String(20))
    activity_name: Mapped[str | None] = mapped_column(String(150))
    planned_start: Mapped[object | None] = mapped_column(Date)
    planned_finish: Mapped[object | None] = mapped_column(Date)
    actual_start: Mapped[object | None] = mapped_column(Date)
    actual_finish: Mapped[object | None] = mapped_column(Date)
    status: Mapped[str | None] = mapped_column(String(50))
    delay_days: Mapped[int | None] = mapped_column(Integer)
    responsible_party: Mapped[str | None] = mapped_column(String(100))


class SiteNote(Base):
    __tablename__ = "site_notes"

    note_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[str | None] = mapped_column(String(20))
    note_date: Mapped[object | None] = mapped_column(Date)
    author: Mapped[str | None] = mapped_column(String(100))
    category: Mapped[str | None] = mapped_column(String(50))
    note_text: Mapped[str | None] = mapped_column(Text)


class RfiLog(Base):
    __tablename__ = "rfi_logs"

    rfi_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    project_id: Mapped[str | None] = mapped_column(String(20))
    submitted_date: Mapped[object | None] = mapped_column(Date)
    question: Mapped[str | None] = mapped_column(Text)
    response: Mapped[str | None] = mapped_column(Text)
    impact_summary: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str | None] = mapped_column(String(50))


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    record_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[str | None] = mapped_column(String(20))
    weather_date: Mapped[object | None] = mapped_column(Date)
    location: Mapped[str | None] = mapped_column(String(150))
    precipitation_inches: Mapped[object | None] = mapped_column(Numeric(5, 2))
    max_wind_mph: Mapped[int | None] = mapped_column(Integer)
    condition_summary: Mapped[str | None] = mapped_column(String(150))


class ChangeOrder(Base):
    __tablename__ = "change_orders"

    co_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    project_id: Mapped[str | None] = mapped_column(String(20))
    title: Mapped[str | None] = mapped_column(String(150))
    reason: Mapped[str | None] = mapped_column(String(100))
    submitted_date: Mapped[object | None] = mapped_column(Date)
    requested_days: Mapped[int | None] = mapped_column(Integer)
    requested_cost: Mapped[object | None] = mapped_column(Numeric(12, 2))
    status: Mapped[str | None] = mapped_column(String(50))
    approved_days: Mapped[int | None] = mapped_column(Integer)
    approved_cost: Mapped[object | None] = mapped_column(Numeric(12, 2))
    summary: Mapped[str | None] = mapped_column(Text)
