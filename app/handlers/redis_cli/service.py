import hashlib
from typing import Optional, List
import time
from datetime import datetime, timedelta, UTC

from app.handlers.auth.interfaces import AsyncRoleService
from app.handlers.coupon.interfaces import AsyncCouponService
from app.handlers.coupon.UOW import SqlAlchemyUnitOfWork
from app.handlers.coupon.schemas import CreateCoupon, OutCoupon, CreateCouponService
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.core.abs.unit_of_work import IUnitOfWorkWallet, IUnitOfWorkCoupon
from app.handlers.session.dependencies import SessionServiceDep
from app.handlers.session.schemas import CheckSessionAccessToken
from app.method.generator_promo import PromoGenerator


#Заготовка под будущие задачи
class RedisService():
    ...