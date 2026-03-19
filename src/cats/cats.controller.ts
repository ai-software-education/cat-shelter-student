import { Controller, Get, Post, Patch, Delete, Body, Param, HttpCode, Query, UseGuards, BadRequestException } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiQuery, ApiParam, ApiResponse, ApiBody, ApiBearerAuth } from '@nestjs/swagger';
import { CatsService } from './cats.service';
import { CreateCatDto } from './dto/create-cat.dto';
import { UpdateCatDto } from './dto/update-cat.dto';
import { ParseIntPipe } from '../common/pipes/parse-int.pipe';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { Role } from '../roles/entities/role.entity';
import { RolesGuard } from 'src/auth/guards/roles.guard'; 
import { Roles } from '../auth/decorators/roles.decorator';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CreateHealthCardDto } from './dto/create-health-card.dto';


@ApiTags('Cats Management')
@Controller('cats')
export class CatsController {
  constructor(
    private readonly catsService: CatsService,
    @InjectRepository(Role)
    private readonly roleRepository: Repository<Role>,
  ) {}

  private validateId(id: string): number {
    if (!/^\d+$/.test(id)) {
      throw new BadRequestException(`Validation failed. ID must be a whole positive integer, but received: ${id}`);
    }
    return parseInt(id, 10);
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Post()
  @ApiOperation({ 
    summary: 'Register a new cat', 
    description: 'Creates a new cat record in the database. The name must be unique to avoid identification errors.' 
  })
  @ApiResponse({ status: 201, description: 'The cat has been successfully registered.' })
  @ApiResponse({ status: 400, description: 'Invalid input data.' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  @ApiResponse({ status: 409, description: 'Conflict: A cat with this name already exists.' })
  create(@Body() dto: CreateCatDto) {
    return this.catsService.create(dto);
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Patch(':id')
  @ApiOperation({ 
    summary: 'Update cat information', 
    description: 'Updates specific fields like name, breed, or history. System fields (isAdopted) should not be modified here.' 
  })
  @ApiParam({ name: 'id', description: 'Unique numerical ID of the cat' })
  @ApiResponse({ status: 200, description: 'Cat info updated successfully.' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  @ApiResponse({ status: 400, description: 'Invalid input or ID' })
  @ApiResponse({ status: 404, description: 'Cat not found.' })
  @ApiResponse({ status: 409, description: 'New name already taken' })
  update(@Param('id') id: string, @Body() dto: UpdateCatDto) {
    const numericId = this.validateId(id);
    return this.catsService.update(numericId, dto);
  }

  @Get(':id')
  @ApiOperation({ 
    summary: 'Get cat details', 
    description: 'Returns full information about a specific cat, including history and owner details if adopted.' 
  })
  @ApiParam({ name: 'id', description: 'Unique numerical ID of the cat' })
  @ApiResponse({ status: 200, description: 'Cat data retrieved successfully.' })
  @ApiResponse ({ status: 400, description: 'Invalid ID format. Expected an integer.'})
  @ApiResponse({ status: 404, description: 'Cat not found.' })
  findOne(@Param('id') id: string) {
    const numericId = this.validateId(id);
    return this.catsService.findOne(numericId);
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Patch(':id/adopt')
  @ApiOperation({ 
    summary: 'Process adoption', 
    description: 'Links a cat to a specific user. Sets adoption status to true and records the current timestamp.' 
  })
  @ApiBody({ 
    schema: { type: 'object', properties: { userId: { type: 'number', description: 'Internal ID of the adopter' } } } 
  })
  @ApiResponse({ status: 200, description: 'Adoption process completed.' })
  @ApiResponse({ status: 400, description: 'Cat is already adopted or invalid user ID.' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  @ApiResponse({ status: 404, description: 'Cat or User not found.' })
  adopt(@Param('id') catId: string, @Body('userId') userId: any) {
    const numericCatId = this.validateId(catId);
    if (!/^\d+$/.test(String(userId))) {
      throw new BadRequestException(`Validation failed. User ID must be a whole integer, but received: ${userId}`);
    }
    return this.catsService.adopt(numericCatId, Number(userId));
  }

  @Get()
  @ApiOperation({ 
    summary: 'Search shelter database', 
    description: 'Returns a list of all cats. Supports filtering by breed, adoption status and age (kittens).' 
  })
  @ApiQuery({ name: 'breed', required: false, description: 'Filter cats by specific breed' })
  @ApiQuery({ name: 'isAdopted', required: false, description: 'Filter by adoption status (true/false)' })
  @ApiQuery({ name: 'isKitten', required: false, type: Boolean, description: 'Filter only cats younger than 1 year' })
  @ApiResponse({ status: 200, description: 'Success' })
  findAll(
    @Query('breed') breed?: string, 
    @Query('isAdopted') isAdopted?: string,
    @Query('isKitten') isKitten?: string
  ) {
    return this.catsService.findAll(breed, isAdopted, isKitten);
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  @ApiBearerAuth()
  @Delete(':id')
  @HttpCode(204)
  @ApiOperation({ summary: 'Remove cat from system', description: 'Permanently deletes a cat record from the database.' })
  @ApiResponse({ status: 204, description: 'Record deleted successfully.' })
  @ApiResponse ({ status: 400, description: 'Invalid ID format. Expected an integer.'})
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  @ApiResponse({ status: 403, description: 'Forbidden: You do not have administrator rights.' })
  @ApiResponse({ status: 404, description: 'Cat not found, cannot delete.' })
  remove(@Param('id') id: string) {
    const numericId = this.validateId(id);
    return this.catsService.remove(numericId);
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Post(':id/health-card')
  @ApiOperation({ 
    summary: 'Create a health card', 
    description: 'Initializes a new medical record for a specific cat. Only one card can exist per cat.' 
  })
  @ApiParam({ name: 'id', description: 'Internal ID of the cat', example: 1 })
  @ApiResponse({ status: 201, description: 'Health card created successfully.' })
  @ApiResponse({ status: 400, description: 'Invalid input data.' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided.' })
  @ApiResponse({ status: 404, description: 'Cat not found.' })
  @ApiResponse({ status: 409, description: 'Conflict: This cat already has a health card.' })
  async createCard(@Param('id') id: string, @Body() dto: CreateHealthCardDto) {
    const numericId = this.validateId(id);
    return this.catsService.createHealthCard(numericId, dto);
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Patch(':id/health-card')
  @ApiOperation({ 
    summary: 'Update health card info', 
    description: 'Modifies medical status, vaccination date, or veterinary notes for an existing card.' 
  })
  @ApiParam({ name: 'id', description: 'Internal ID of the cat', example: 1 })
  @ApiResponse({ status: 200, description: 'Health card updated successfully.' })
  @ApiResponse({ status: 400, description: 'Invalid input or ID format.' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided.' })
  @ApiResponse({ status: 404, description: 'Health card not found for this cat.' })
  async updateCard(@Param('id') id: string, @Body() dto: CreateHealthCardDto) {
    const numericId = this.validateId(id);
    return this.catsService.updateHealthCard(numericId, dto);
  }
}