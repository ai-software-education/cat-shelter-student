import { Injectable, CanActivate, ExecutionContext, ForbiddenException } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.get<string[]>('roles', context.getHandler());
    if (!requiredRoles) return true;
  
    const { user } = context.switchToHttp().getRequest();
    const isAdmin = user.role === 'admin' || user.roleId === 2;
  
    if (requiredRoles.includes('admin') && !isAdmin) {
      throw new ForbiddenException('Forbidden: You do not have administrator rights.');
    }
  
    return true;
  }
}