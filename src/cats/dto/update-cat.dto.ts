import { ApiPropertyOptional } from '@nestjs/swagger';
import { IsInt, IsOptional, IsString, Min, MinLength } from 'class-validator';

export class UpdateCatDto {
  @ApiPropertyOptional({ example: 'Barsik', description: 'Updated name of the cat' })
  @IsOptional() 
  @IsString() 
  @MinLength(2)
  readonly name?: string;

  @ApiPropertyOptional({ example: 3, description: 'Updated age of the cat' })
  @IsOptional() 
  @IsInt() 
  @Min(0)
  readonly age?: number;

  @ApiPropertyOptional({ example: 'Siamese', description: 'Updated breed' })
  @IsOptional() 
  @IsString() 
  readonly breed?: string;

  @ApiPropertyOptional({ example: 'Found in 2024', description: 'Updated history' })
  @IsOptional() 
  @IsString() 
  readonly history?: string;

  @ApiPropertyOptional({ example: 'Very friendly cat', description: 'Updated description' })
  @IsOptional() 
  @IsString() 
  readonly description?: string;
}