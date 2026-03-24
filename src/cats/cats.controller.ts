import { Controller, Get, Post, Delete, Body, Param, HttpCode, ParseIntPipe } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiParam } from '@nestjs/swagger';
import { CatsService } from './cats.service';
import { CreateCatDto } from './dto/create-cat.dto';

@ApiTags('Cats Management')
@Controller('cats')
export class CatsController {
  constructor(private readonly catsService: CatsService) {}

  @Post()
  @ApiOperation({ 
    summary: 'Register a new cat', 
    description: 'Creates a new cat record in the database. The name must be unique to avoid identification errors.' 
  })
  @ApiResponse({ status: 201, description: 'The cat has been successfully registered.' })
  @ApiResponse({ status: 400, description: 'Invalid input data.' })
  @ApiResponse({ status: 409, description: 'Conflict: A cat with this name already exists.' })
  create(@Body() dto: CreateCatDto) {
    return this.catsService.create(dto);
  }

  @Get()
  @ApiOperation({ summary: 'Get all cats in the shelter' })
  @ApiResponse({ status: 200, description: 'Return list of cats.' })
  findAll() {
    return this.catsService.findAll();
  }

  @Get(':id')
  @ApiOperation({ 
    summary: 'Get cat details', 
    description: 'Retrieves full information about a specific cat by its unique ID.' 
  })
  @ApiParam({ name: 'id', description: 'Unique numerical ID of the cat', example: 1 })
  @ApiResponse({ status: 200, description: 'Cat data retrieved successfully.' })
  @ApiResponse({ status: 400, description: 'Invalid ID format. Expected an integer.' })
  @ApiResponse({ status: 404, description: 'Cat not found.' })
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.catsService.findOne(id);
  }

  @Delete(':id')
  @HttpCode(204)
  @ApiOperation({ summary: 'Remove a cat from the database' })
  @ApiResponse({ status: 204, description: 'Cat deleted.' })
  @ApiResponse({ status: 400, description: 'Invalid ID format.' })
  @ApiResponse({ status: 404, description: 'Cat not found.' })
  remove(@Param('id', ParseIntPipe) id: number) {
    return this.catsService.remove(id);
  }
}