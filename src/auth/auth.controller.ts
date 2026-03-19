import { Controller, Post, Body, HttpCode } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { AuthService } from './auth.service';
import { CreateUserDto } from '../users/dto/create-user.dto';
import { LoginDto } from './dto/login.dto'

@ApiTags('Authentication')
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('register')
  @ApiOperation({ summary: 'Register a new user' })
  @ApiResponse({ status: 201, description: 'User registered and token returned' })
  @ApiResponse({ status: 400, description: 'Validation error (e.g. short password or empty fields).' })
  @ApiResponse({ status: 409, description: 'A user with this login already exists.' })
  register(@Body() dto: CreateUserDto) {
    return this.authService.register(dto);
  }

  @Post('login')
  @HttpCode(200)
  @ApiOperation({ summary: 'Login with credentials' })
  @ApiResponse({ status: 200, description: 'Returns JWT token.' })
  @ApiResponse({ status: 400, description: 'Invalid input format or missing fields.' })
  @ApiResponse({ status: 401, description: 'Invalid login or password.' })
  login(@Body() dto: LoginDto) {
    return this.authService.login(dto);
  }
}