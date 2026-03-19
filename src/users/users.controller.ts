import { Controller, Get, Post, Body, Param, Delete, ParseIntPipe, HttpCode, UseGuards, Req, ForbiddenException } from '@nestjs/common';
import { UsersService } from './users.service';
import { UserEntity } from './entities/user.entity';
import { ApiTags, ApiOperation, ApiResponse, ApiParam, ApiBearerAuth } from '@nestjs/swagger';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Role } from '../roles/entities/role.entity';
import { RolesGuard } from 'src/auth/guards/roles.guard'; 
import { Roles } from '../auth/decorators/roles.decorator';

@ApiTags('Users Management')
@Controller('users')
export class UsersController {
  constructor(
    private readonly usersService: UsersService,
    @InjectRepository(Role)
    private readonly roleRepository: Repository<Role>,
  ) {}

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Get()
  @ApiOperation({ summary: 'List all users', description: 'Returns a list of all registered users.' })
  @ApiResponse({ status: 200, description: 'Success' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  findAll() {
    return this.usersService.findAll();
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Get(':id')
  @ApiOperation({ 
    summary: 'Get user profile', 
    description: 'Retrieves user details and the list of cats they have adopted.' 
  })
  @ApiResponse({ status: 200, description: 'User found.' })
  @ApiResponse({ status: 400, description: 'Invalid ID format provided.' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  @ApiResponse({ status: 404, description: 'User not found.' })
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.usersService.findOne(id);
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Get(':id/cats')
  @ApiOperation({ 
    summary: 'Get all cats adopted by a specific user',
    description: 'Returns user profile with the list of their adopted cats.' 
  })
  @ApiParam({ name: 'id', description: 'User ID', example: 1 })
  @ApiResponse({ status: 200, description: 'Success', type: UserEntity })
  @ApiResponse({ status: 400, description: 'Invalid ID' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  @ApiResponse({ status: 404, description: 'User not found' })
  getUserCats(@Param('id', ParseIntPipe) id: number) {
    return this.usersService.findUserCats(id);
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Delete(':id')
  @HttpCode(204)
  @ApiOperation({ 
    summary: 'Delete user profile', 
    description: 'Permanently removes a user. Note: Associated cats will remain in the system but will become ownerless (SET NULL).' 
  })
  @ApiParam({ name: 'id', description: 'User ID to delete', example: 1 })
  @ApiResponse({ status: 204, description: 'User deleted successfully.' })
  @ApiResponse({ status: 400, description: 'Invalid ID' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  @ApiResponse({ status: 403, description: 'Access denied. You can only delete your own profile'})
  @ApiResponse({ status: 404, description: 'User not found.' })
  async remove(@Param('id', ParseIntPipe) id: number, @Req() req) {
    const currentUser = req.user;
    const isAdmin = currentUser.role === 'admin' || currentUser.roleId === 2;
    const isOwner = currentUser.userId === id;
    if (!isAdmin && !isOwner) {
      throw new ForbiddenException('Access denied. You can only delete your own profile');
    }
    return this.usersService.remove(id);
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @Post(':id/make-admin')
  @ApiOperation({ 
    summary: 'Give admin rights to user', 
    description: 'Changes the user role to Admin. Restricted to users with existing Admin privileges.' 
  })
  @ApiParam({ name: 'id', description: 'User ID to be promoted', example: 2 })
  @ApiResponse({ status: 201, description: 'User has been successfully promoted to Admin.' })
  @ApiResponse({ status: 400, description: 'Invalid ID format provided.' })
  @ApiResponse({ status: 401, description: 'Unauthorized: Token is missing or invalid.' })
  @ApiResponse({ status: 403, description: 'Forbidden: You do not have administrator rights.' })
  @ApiResponse({ status: 404, description: 'User not found.' })
  async makeAdmin(@Param('id', ParseIntPipe) id: number) {
     const adminRole = await this.roleRepository.findOne({ where: { name: 'admin' } });
     return this.usersService.changeRole(id, adminRole);
  }
}