import { Controller, Get, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { StatsService } from './stats.service';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';


@ApiTags('Statistics')
@Controller('stats')
export class StatsController {
  constructor(private readonly statsService: StatsService) {}

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Get('summary')
  @ApiOperation({ summary: 'Get general shelter metrics' })
  @ApiResponse({ status: 200, description: 'Total counts and adoption percentage' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  getSummary() {
    return this.statsService.getGeneralSummary();
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Get('breeds')
  @ApiOperation({ summary: 'Distribution of cats by breeds' })
  @ApiResponse({ status: 200, description: 'List of breeds with counts' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  getBreedStats() {
    return this.statsService.getBreedDistribution();
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth()
  @Get('top-adopters')
  @ApiOperation({ 
    summary: 'Get most active adopters', 
    description: 'Returns top 5 users who have adopted the most cats' 
  })
  @ApiResponse({ status: 200, description: 'List of top adopters' })
  @ApiResponse({ status: 401, description: 'Not authorized: No token provided or token invalid.' })
  getTopAdopters() {
    return this.statsService.getTopAdopters();
  }
}